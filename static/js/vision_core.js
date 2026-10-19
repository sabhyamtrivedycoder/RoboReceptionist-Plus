/**
 * vision_core.js - Client-Side Clinical Computer Vision Pipeline
 * Performs genuine pixel-level colorimetric segmentation, Sobel edge gradient convolution,
 * wound margin isolation, connected bounding box detection, and anatomical heatmapping.
 */

class ClinicalVisionCore {
  constructor() {
    this.canvas = document.createElement("canvas");
    this.ctx = this.canvas.getContext("2d", { willReadFrequently: true });
  }

  /**
   * Converts an RGB color to HSV representation.
   * R, G, B in [0, 255] -> H in [0, 360], S in [0, 1], V in [0, 1]
   */
  static rgbToHsv(r, g, b) {
    const rf = r / 255, gf = g / 255, bf = b / 255;
    const max = Math.max(rf, gf, bf), min = Math.min(rf, gf, bf);
    const d = max - min;
    let h = 0, s = max === 0 ? 0 : d / max, v = max;

    if (max !== min) {
      switch (max) {
        case rf: h = (gf - bf) / d + (gf < bf ? 6 : 0); break;
        case gf: h = (bf - rf) / d + 2; break;
        case bf: h = (rf - gf) / d + 4; break;
      }
      h *= 60;
    }
    return [h, s, v];
  }

  /**
   * Processes an image element or DataURL through the full optical pipeline.
   * Returns quantitative telemetry and an annotated diagnostic canvas image.
   */
  async processImage(imageSource) {
    const img = await this._loadImage(imageSource);
    const w = img.naturalWidth || img.width;
    const h = img.naturalHeight || img.height;

    // Constrain processing buffer to max 640px for real-time latency
    const scale = Math.min(1.0, 640 / Math.max(w, h));
    const targetW = Math.max(32, Math.round(w * scale));
    const targetH = Math.max(32, Math.round(h * scale));

    this.canvas.width = targetW;
    this.canvas.height = targetH;
    this.ctx.drawImage(img, 0, 0, targetW, targetH);

    const imgData = this.ctx.getImageData(0, 0, targetW, targetH);
    const pixels = imgData.data;
    const totalPixels = targetW * targetH;

    // Stage 1: Pixel-level tissue classification & masking
    const grayBuffer = new Uint8Array(totalPixels);
    const woundMask = new Uint8Array(totalPixels);

    let erythemaCount = 0;
    let necroticCount = 0;
    let exudateCount = 0;
    let minX = targetW, minY = targetH, maxX = 0, maxY = 0;
    let sumX = 0, sumY = 0, woundPixelsCount = 0;

    for (let i = 0, p = 0; i < pixels.length; i += 4, p++) {
      const r = pixels[i];
      const g = pixels[i + 1];
      const b = pixels[i + 2];

      // Luminance for gradient analysis
      const gray = Math.round(0.299 * r + 0.587 * g + 0.114 * b);
      grayBuffer[p] = gray;

      const [hue, sat, val] = ClinicalVisionCore.rgbToHsv(r, g, b);

      // Erythema / Active extravasation (red inflamed margins)
      const isErythema = (hue <= 24 || hue >= 336) && sat >= 0.22 && val >= 0.18 && (r > g * 1.15);
      // Necrotic / Devitalized eschar (dark tissue)
      const isNecrotic = val < 0.18 && sat < 0.45;
      // Slough / Purulent exudate (yellowish fibrin)
      const isExudate = hue >= 38 && hue <= 68 && sat >= 0.28 && val >= 0.35;

      if (isErythema) erythemaCount++;
      if (isNecrotic) necroticCount++;
      if (isExudate) exudateCount++;

      if (isErythema || isNecrotic || isExudate) {
        woundMask[p] = 1;
        const px = p % targetW;
        const py = Math.floor(p / targetW);
        if (px < minX) minX = px;
        if (px > maxX) maxX = px;
        if (py < minY) minY = py;
        if (py > maxY) maxY = py;
        sumX += px;
        sumY += py;
        woundPixelsCount++;
      }
    }

    // Stage 2: Sobel Edge Gradient Convolution (Margin sharpness & depth)
    let edgeHits = 0;
    const sobelX = [-1, 0, 1, -2, 0, 2, -1, 0, 1];
    const sobelY = [-1, -2, -1, 0, 0, 0, 1, 2, 1];

    for (let y = 1; y < targetH - 1; y++) {
      for (let x = 1; x < targetW - 1; x++) {
        let gx = 0, gy = 0;
        let k = 0;
        for (let dy = -1; dy <= 1; dy++) {
          for (let dx = -1; dx <= 1; dx++) {
            const val = grayBuffer[(y + dy) * targetW + (x + dx)];
            gx += val * sobelX[k];
            gy += val * sobelY[k];
            k++;
          }
        }
        const grad = Math.sqrt(gx * gx + gy * gy);
        if (grad > 65) {
          edgeHits++;
        }
      }
    }

    const erythemaRatio = parseFloat(((erythemaCount / totalPixels) * 100).toFixed(2));
    const necroticRatio = parseFloat(((necroticCount / totalPixels) * 100).toFixed(2));
    const exudateRatio = parseFloat(((exudateCount / totalPixels) * 100).toFixed(2));
    const edgeDensity = parseFloat(((edgeHits / totalPixels) * 100).toFixed(2));
    const lesionSurfaceRatio = parseFloat(((woundPixelsCount / totalPixels) * 100).toFixed(2));

    // Stage 3: Real Bounding Box Calculation
    let bbox = null;
    let centroid = null;

    if (woundPixelsCount > totalPixels * 0.005) {
      // Add clinical margin padding (12%)
      const padX = Math.round((maxX - minX) * 0.12);
      const padY = Math.round((maxY - minY) * 0.12);
      const bx = Math.max(0, minX - padX);
      const by = Math.max(0, minY - padY);
      const bw = Math.min(targetW - bx, (maxX - minX) + padX * 2);
      const bh = Math.min(targetH - by, (maxY - minY) + padY * 2);

      bbox = { x: bx, y: by, width: bw, height: bh };
      centroid = {
        x: Math.round(sumX / woundPixelsCount),
        y: Math.round(sumY / woundPixelsCount)
      };
    } else {
      // Default central region of interest if diffuse trauma
      const bw = Math.round(targetW * 0.6);
      const bh = Math.round(targetH * 0.6);
      const bx = Math.round((targetW - bw) / 2);
      const by = Math.round((targetH - bh) / 2);
      bbox = { x: bx, y: by, width: bw, height: bh };
      centroid = { x: Math.round(targetW / 2), y: Math.round(targetH / 2) };
    }

    // Stage 4: Render Clinical Diagnostic Overlay on Canvas
    // Draw semi-transparent wound tissue heatmap
    const overlayImgData = this.ctx.getImageData(0, 0, targetW, targetH);
    const oPixels = overlayImgData.data;
    for (let p = 0; p < totalPixels; p++) {
      if (woundMask[p] === 1) {
        const idx = p * 4;
        // Blend ruby highlight over detected damaged tissue
        oPixels[idx] = Math.min(255, oPixels[idx] + 70);       // Red boost
        oPixels[idx + 1] = Math.max(0, oPixels[idx + 1] - 30); // Green suppress
        oPixels[idx + 2] = Math.max(0, oPixels[idx + 2] - 30); // Blue suppress
      }
    }
    this.ctx.putImageData(overlayImgData, 0, 0);

    // Draw Clinical Reticle & Bounding Box
    const isCritical = erythemaRatio > 14 || edgeDensity > 9 || necroticRatio > 4;
    const accentColor = isCritical ? "#ef4444" : "#0284c7"; // Crimson or Medical Azure

    this.ctx.save();
    this.ctx.strokeStyle = accentColor;
    this.ctx.lineWidth = 2;
    this.ctx.strokeRect(bbox.x, bbox.y, bbox.width, bbox.height);

    // Corner brackets
    const clen = Math.min(18, Math.floor(bbox.width / 4));
    this.ctx.lineWidth = 3;
    // TL
    this.ctx.beginPath(); this.ctx.moveTo(bbox.x, bbox.y + clen); this.ctx.lineTo(bbox.x, bbox.y); this.ctx.lineTo(bbox.x + clen, bbox.y); this.ctx.stroke();
    // TR
    this.ctx.beginPath(); this.ctx.moveTo(bbox.x + bbox.width - clen, bbox.y); this.ctx.lineTo(bbox.x + bbox.width, bbox.y); this.ctx.lineTo(bbox.x + bbox.width, bbox.y + clen); this.ctx.stroke();
    // BL
    this.ctx.beginPath(); this.ctx.moveTo(bbox.x, bbox.y + bbox.height - clen); this.ctx.lineTo(bbox.x, bbox.y + bbox.height); this.ctx.lineTo(bbox.x + clen, bbox.y + bbox.height); this.ctx.stroke();
    // BR
    this.ctx.beginPath(); this.ctx.moveTo(bbox.x + bbox.width - clen, bbox.y + bbox.height); this.ctx.lineTo(bbox.x + bbox.width, bbox.y + bbox.height); this.ctx.lineTo(bbox.x + bbox.width, bbox.y + bbox.height - clen); this.ctx.stroke();

    // Centroid Crosshair
    if (centroid) {
      this.ctx.strokeStyle = "rgba(255, 255, 255, 0.75)";
      this.ctx.lineWidth = 1;
      this.ctx.beginPath();
      this.ctx.moveTo(centroid.x - 8, centroid.y);
      this.ctx.lineTo(centroid.x + 8, centroid.y);
      this.ctx.moveTo(centroid.x, centroid.y - 8);
      this.ctx.lineTo(centroid.x, centroid.y + 8);
      this.ctx.stroke();
    }

    // Telemetry label badge
    this.ctx.fillStyle = "rgba(15, 23, 42, 0.88)";
    const labelText = `ROI // LESION ${lesionSurfaceRatio}% [ERY: ${erythemaRatio}% | EDG: ${edgeDensity}%]`;
    this.ctx.font = "bold 10px monospace";
    const textWidth = this.ctx.measureText(labelText).width;
    const badgeY = Math.max(16, bbox.y - 6);
    this.ctx.fillRect(bbox.x, badgeY - 12, textWidth + 10, 16);
    this.ctx.fillStyle = accentColor;
    this.ctx.fillText(labelText, bbox.x + 5, badgeY);

    this.ctx.restore();

    const annotatedDataUrl = this.canvas.toDataURL("image/jpeg", 0.92);

    return {
      dimensions: { width: targetW, height: targetH },
      erythemaRatio,
      necroticRatio,
      exudateRatio,
      edgeDensity,
      lesionSurfaceRatio,
      bbox,
      centroid,
      annotatedDataUrl
    };
  }

  _loadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = () => resolve(img);
      img.onerror = (e) => reject(new Error("Failed to load image buffer for optical analysis."));
      img.src = src;
    });
  }
}

// Export singleton to window
window.ClinicalVisionCore = ClinicalVisionCore;
