/**
 * specialists_roster.js - Hospital Specialist Registry & Dispatch Engine
 * Matches patient diagnosis and ESI priority against on-call medical specialists.
 */

class SpecialistRegistry {
  static ROSTER = [
    {
      id: 1,
      name: "Dr. Vikram Sen",
      title: "Senior Trauma & Critical Care Surgeon",
      department: "Emergency Trauma & Burn Surgery",
      specialty: "Trauma & Emergency",
      subSpecialty: "Acute Resuscitation & Complex Dermal Closure",
      license: "MC-TRAUMA-90214",
      roomNumber: "Trauma Bay 01",
      phone: "+91 98112-40912",
      status: "ON-DUTY // READY",
      experienceYears: 18,
      rating: 4.95,
      avatarUrl: "https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&q=80&w=260"
    },
    {
      id: 2,
      name: "Dr. Ananya Roy",
      title: "Chief of Dermatology & Burn Reconstruction",
      department: "Dermatology & Burn Care",
      specialty: "Dermatology & Burn Care",
      subSpecialty: "Thermal Trauma, Grafting & Blistering Debridement",
      license: "MC-DERM-44109",
      roomNumber: "Burn Unit Suite 04",
      phone: "+91 98223-10944",
      status: "ON-DUTY // READY",
      experienceYears: 14,
      rating: 4.92,
      avatarUrl: "https://images.unsplash.com/photo-1594824813583-8a39f604ec28?auto=format&fit=crop&q=80&w=260"
    },
    {
      id: 3,
      name: "Dr. Marcus Vance",
      title: "Attending Orthopedic Trauma Surgeon",
      department: "Orthopedic Surgery & Sports Trauma",
      specialty: "Orthopedic Surgery",
      subSpecialty: "Closed Reduction, Complex Fractures & Joint Stabilization",
      license: "MC-ORTHO-88312",
      roomNumber: "Orthopedic Bay 02",
      phone: "+91 98334-55120",
      status: "ON-DUTY // READY",
      experienceYears: 16,
      rating: 4.88,
      avatarUrl: "https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&q=80&w=260"
    },
    {
      id: 4,
      name: "Dr. Elena Rostova",
      title: "Consultant Vitreoretinal & Cornea Surgeon",
      department: "Emergency Ophthalmology",
      specialty: "Ophthalmology",
      subSpecialty: "Ocular Chemical Burns, Corneal Lacerations & Slit-Lamp Microsurgery",
      license: "MC-OPHTH-71203",
      roomNumber: "Eye Emergency Clinic 101",
      phone: "+91 98445-66781",
      status: "ON-DUTY // READY",
      experienceYears: 12,
      rating: 4.96,
      avatarUrl: "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&q=80&w=260"
    },
    {
      id: 5,
      name: "Dr. Rajesh Kothari",
      title: "Lead Emergency Medicine Physician",
      department: "Emergency Medicine & Acute Resuscitation",
      specialty: "General Emergency Medicine",
      subSpecialty: "Polytrauma Triage, Closed Hematomas & Toxic Exposure",
      license: "MC-ER-10294",
      roomNumber: "Emergency Assessment Room 03",
      phone: "+91 98778-99012",
      status: "ON-DUTY // READY",
      experienceYears: 20,
      rating: 4.91,
      avatarUrl: "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&q=80&w=260"
    },
    {
      id: 6,
      name: "Dr. Sofia Chen",
      title: "Microvascular & Plastic Reconstructive Surgeon",
      department: "Plastic & Reconstructive Surgery",
      specialty: "Trauma & Emergency",
      subSpecialty: "Aesthetic Facial Lacerations & Tendon Micro-repair",
      license: "MC-PLAST-55291",
      roomNumber: "Trauma Bay 03",
      phone: "+91 98991-22340",
      status: "ON-DUTY // READY",
      experienceYears: 11,
      rating: 4.89,
      avatarUrl: "https://images.unsplash.com/photo-1582750433449-648ed127bb54?auto=format&fit=crop&q=80&w=260"
    }
  ];

  /**
   * Matches doctors from the roster given the required specialty string.
   */
  static matchSpecialists(requiredSpecialty) {
    if (!requiredSpecialty) return this.ROSTER.slice(0, 3);

    const query = requiredSpecialty.toLowerCase();
    const scored = this.ROSTER.map(doc => {
      let score = 0;
      const spec = doc.specialty.toLowerCase();
      const sub = doc.subSpecialty.toLowerCase();
      const dept = doc.department.toLowerCase();

      if (spec === query) score += 100;
      else if (spec.includes(query) || query.includes(spec)) score += 60;
      if (sub.includes(query)) score += 40;
      if (dept.includes(query)) score += 30;

      score += doc.rating * 5;
      score += doc.experienceYears;

      return { doc, score };
    });

    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, 3).map(s => s.doc);
  }
}

// Export singleton to window
window.SpecialistRegistry = SpecialistRegistry;
