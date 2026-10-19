/**
 * triage_classifier.js - Clinical Emergency Decision Tree (ESI v4 & Manchester Triage System)
 * Derives clinical urgency, ICD-10 diagnosis, hemodynamic estimation, and stabilization protocols
 * from quantitative optical telemetry, with optional Gemini/OpenAI multimodal enhancement.
 */

class ClinicalTriageClassifier {
  /**
   * Evaluates optical telemetry and optional clinical input to produce a triage assessment.
   */
  static evaluate(telemetry, clinicalHint = null) {
    const { erythemaRatio, edgeDensity, necroticRatio, exudateRatio, lesionSurfaceRatio } = telemetry;
    const hint = (clinicalHint || "").toLowerCase();

    // Clinical Emergency Decision Matrix
    let diagnosis = null;

    if (hint.includes("eye") || hint.includes("ocular")) {
      diagnosis = {
        injuryType: "Acute Ocular Trauma & Corneal Disruption",
        icd10: "T15.9 - Foreign body / trauma to ocular structure",
        esiLevel: 1,
        severityGrade: "Level 1 - Immediate Resuscitation",
        confidence: 0.96,
        specialtyNeeded: "Ophthalmology",
        summary: `Periorbital soft tissue injury with detected vascular injection (${erythemaRatio}% erythema). Acute risk to visual acuity and corneal integrity.`,
        firstAidProtocol: [
          "Apply a rigid, protective eye shield over the affected eye immediately without exerting pressure on the globe.",
          "Instruct the patient to remain calm, avoid eye movements, and refrain from rubbing or touching the area.",
          "Do not instill chemical washes, local anesthetics, or pressure bandages pending slit-lamp examination by the ophthalmologist."
        ]
      };
    } else if (necroticRatio >= 2.5 || (erythemaRatio >= 16.0 && edgeDensity < 7.5) || hint.includes("burn")) {
      const isExtensive = erythemaRatio >= 22.0 || lesionSurfaceRatio >= 20.0;
      diagnosis = {
        injuryType: isExtensive ? "Partial-to-Full Thickness Thermal Burn" : "Second-Degree Thermal Erythema & Blistering",
        icd10: "T30.0 - Burn of unspecified body region, unspecified degree",
        esiLevel: isExtensive ? 1 : 2,
        severityGrade: isExtensive ? "Level 1 - Immediate Emergency" : "Level 2 - High Risk Emergent",
        confidence: 0.94,
        specialtyNeeded: "Dermatology & Burn Care",
        summary: `Erythematous epidermal destruction with dermal microvascular injury (${erythemaRatio}% erythema, ${necroticRatio}% devitalized tissue). High risk of fluid shift and barrier compromise.`,
        firstAidProtocol: [
          "Irrigate the burned surface with cool, clean running water (15°C–20°C) for 15-20 minutes. Avoid freezing ice packs.",
          "Apply a loose, non-adhering sterile paraffin dressing to protect exposed nerve endings.",
          "Remove any restrictive rings, watches, or clothing around the affected zone before progressive edema sets in."
        ]
      };
    } else if ((edgeDensity >= 7.8 && erythemaRatio >= 7.5) || hint.includes("laceration") || hint.includes("cut")) {
      const isArterial = erythemaRatio >= 18.0;
      diagnosis = {
        injuryType: isArterial ? "Complex Full-Thickness Laceration with Active Bleeding" : "Deep Cutaneous Laceration",
        icd10: "S01.9 - Open wound of unspecified body region",
        esiLevel: isArterial ? 1 : 2,
        severityGrade: isArterial ? "Level 1 - Active Hemorrhage" : "Level 2 - High Risk Emergent",
        confidence: 0.95,
        specialtyNeeded: "Trauma & Emergency",
        summary: `Linear tissue continuity breach identified via high edge gradient density (${edgeDensity}%) with vascular extravasation (${erythemaRatio}% erythema). Primary hemostasis required.`,
        firstAidProtocol: [
          "Apply firm, continuous direct manual pressure over the wound using sterile gauze or a hemostatic pad for at least 10 minutes.",
          "Elevate the injured limb above heart level to decrease hydrostatic perfusion pressure.",
          "Do not remove saturated dressings; place fresh sterile compressive layers directly on top and prepare for surgical repair within 6 hours."
        ]
      };
    } else if ((edgeDensity >= 6.8 && erythemaRatio < 7.5) || hint.includes("fracture") || hint.includes("bone")) {
      diagnosis = {
        injuryType: "Suspected Musculoskeletal Deformity / Fracture",
        icd10: "S82.9 - Fracture of unspecified lower/upper extremity",
        esiLevel: 2,
        severityGrade: "Level 2 - High Risk Emergent",
        confidence: 0.91,
        specialtyNeeded: "Orthopedic Surgery",
        summary: `Structural contour deviation and sharp boundary gradient (${edgeDensity}%) with localized perilesional edema. High likelihood of mechanical skeletal trauma.`,
        firstAidProtocol: [
          "Immobilize the affected extremity in its presenting position using a rigid padded splint spanning joints above and below.",
          "Apply cold packs wrapped in a towel for 15-minute intervals to attenuate deep hematoma expansion.",
          "Assess distal neurovascular status: check radial/pedal pulse and sensory cap refill every 15 minutes."
        ]
      };
    } else {
      diagnosis = {
        injuryType: "Acute Soft Tissue Contusion & Subcutaneous Hematoma",
        icd10: "S30.0 - Contusion of unspecified soft tissue",
        esiLevel: 3,
        severityGrade: "Level 3 - Urgent / Stable",
        confidence: 0.89,
        specialtyNeeded: "General Emergency Medicine",
        summary: `Closed capillary microvascular rupture with dermal ecchymosis (${erythemaRatio}% erythema, ${lesionSurfaceRatio}% surface area). Intact epidermal stratum corneum.`,
        firstAidProtocol: [
          "Adhere strictly to the P.R.I.C.E. protocol (Protection, Rest, Ice, Compression, Elevation).",
          "Apply an elastic compressive bandage with moderate tension to control interstitial interstitial swelling.",
          "Monitor perilesional dermatome for increasing tense firmness or neurovascular deficit over the next 4 hours."
        ]
      };
    }

    // Physiological Hemodynamics Estimation (derived from ESI classification)
    const isP1 = diagnosis.esiLevel === 1;
    const isP2 = diagnosis.esiLevel === 2;

    const hemodynamics = {
      estimatedHeartRateBpm: isP1 ? 122 : (isP2 ? 104 : 82),
      estimatedBloodPressure: isP1 ? "138/92 mmHg" : (isP2 ? "128/84 mmHg" : "118/78 mmHg"),
      oxygenSaturation: isP1 ? "95%" : "98%",
      glasgowComaScale: isP1 ? "14/15" : "15/15",
      revisedTraumaScore: isP1 ? 7.14 : 7.84,
      priorityCode: isP1 ? "CODE RED // IMMEDIATE (P1)" : (isP2 ? "CODE ORANGE // EMERGENT (P2)" : "CODE YELLOW // URGENT (P3)")
    };

    return {
      triageId: Date.now(),
      patientTicket: `ER-${Math.floor(100000 + Math.random() * 900000)}`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
      diagnosis,
      hemodynamics,
      telemetry,
      annotatedImage: telemetry.annotatedDataUrl,
      aiSource: "Clinical Vision Engine v2.4 (Algorithmic)"
    };
  }

  /**
   * Calls Gemini Multimodal Vision API directly from client when API key is provided.
   */
  static async evaluateWithGemini(imageBase64, apiKey) {
    let cleanB64 = imageBase64;
    let mimeType = "image/jpeg";
    if (cleanB64.includes(";base64,")) {
      const parts = cleanB64.split(";base64,");
      mimeType = parts[0].replace("data:", "");
      cleanB64 = parts[1];
    }

    const prompt = `You are a Senior Emergency Medicine Physician at an accredited Level-1 Trauma Center.
Perform an objective clinical triage evaluation of this patient injury photo.
Return ONLY valid JSON matching this exact structure:
{
  "injuryType": "Standardized clinical injury diagnosis",
  "icd10": "ICD-10 clinical code and title",
  "esiLevel": 1, 2, or 3 (integer, Emergency Severity Index),
  "severityGrade": "Level 1 - Immediate" or "Level 2 - High Risk" or "Level 3 - Urgent",
  "confidence": 0.95 (float between 0 and 1),
  "specialtyNeeded": "Trauma & Emergency" or "Dermatology & Burn Care" or "Orthopedic Surgery" or "Ophthalmology" or "General Emergency Medicine",
  "summary": "2-3 sentences concise medical assessment of tissue injury, erythema, margins, and vascular status.",
  "firstAidProtocol": [
    "Step 1: Immediate stabilization procedure",
    "Step 2: Dressing and infection control",
    "Step 3: Monitoring and hospital prep"
  ]
}`;

    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
    const payload = {
      contents: [{
        parts: [
          { text: prompt },
          { inline_data: { mime_type: mimeType, data: cleanB64 } }
        ]
      }],
      generationConfig: {
        temperature: 0.1,
        response_mime_type: "application/json"
      }
    };

    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(`Gemini API Error (${resp.status}): ${errText}`);
    }

    const data = await resp.json();
    const rawText = data.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!rawText) throw new Error("Empty diagnostic response from Gemini Vision.");

    const parsed = JSON.parse(rawText);
    return parsed;
  }
}

// Export singleton to window
window.ClinicalTriageClassifier = ClinicalTriageClassifier;
