from pathlib import Path
from textwrap import wrap

PDF_TEMPLATE = b"""%PDF-1.4
%\xe2\xe3\xcf\xd3
"""


def pdf_escape(text: str) -> bytes:
    return (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .encode("latin1", errors="replace")
    )


def build_page_lines(lines, title):
    wrapped = [title, ""]
    for line in lines:
        if line.startswith("SECTION:" ):
            wrapped.append(line.split(":", 1)[1].upper())
            continue
        if line.startswith("- "):
            wrapped.append(line)
            continue
        wrapped.extend(wrap(line, 95))
    return wrapped


def build_page(content_lines):
    stream_lines = [b"BT /F1 10 Tf 50 800 Td"]
    for line in content_lines:
        if not line.strip():
            stream_lines.append(b"0 -14 Td")
            continue
        escaped = pdf_escape(line)
        stream_lines.append(b"(" + escaped + b") Tj")
        stream_lines.append(b"0 -14 Td")
    stream_lines.append(b"ET")
    return b"\n".join(stream_lines)


def build_pdf(title, pages):
    objects = []
    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [")

    page_objs = []
    for i, page_lines in enumerate(pages):
        page_obj_num = 3 + i * 2
        content_obj_num = page_obj_num + 1
        page_objs.append(f"{page_obj_num} 0 R")
        stream = build_page(page_lines)
        objects.append(
            f"{page_obj_num} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 {page_obj_num + 2} 0 R >> >> /Contents {content_obj_num} 0 R >>\nendobj\n".encode()
        )
        objects.append(
            f"{content_obj_num} 0 obj\n<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"\nendstream\nendobj\n"
        )
        objects.append(
            f"{page_obj_num + 2} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n".encode()
        )

    objects[1] = (b"2 0 obj\n<< /Type /Pages /Kids [" + " ".join(page_objs).encode() + f" ] /Count {len(pages)} >>\nendobj\n".encode())

    output = bytearray(PDF_TEMPLATE)
    xref_positions = []
    for obj in objects:
        xref_positions.append(len(output))
        output.extend(obj)

    xref_start = len(output)
    output.extend(b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1))
    for pos in xref_positions:
        output.extend(b"%010d 00000 n \n" % pos)
    output.extend(
        b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"
        % (len(objects) + 1, xref_start)
    )
    return bytes(output)


def build_resume_pages(title, sections):
    pages = []
    current = []
    current_lines = 0
    for section_title, lines in sections:
        if current_lines + len(lines) + 2 > 34 and current:
            pages.append([title] + current)
            current = []
            current_lines = 0
        current.append(section_title)
        current.extend(lines)
        current.append("")
        current_lines += len(lines) + 2
    if current:
        pages.append([title] + current)
    return pages


def main():
    ats_sections = [
        ("SECTION:Professional Summary", [
            "AI-assisted full stack developer focused on production-ready web platforms, modern SaaS architecture, and scalable Laravel/Next.js systems.",
            "I quickly understand new frameworks using AI-assisted development while maintaining production quality, maintainability, and performance.",
            "Experience includes real client work, admin dashboards, school and college management systems, e-commerce systems, SEO-focused landing pages, and live deployment on VPS and Docker."
        ]),
        ("SECTION:Education & Background", [
            "Born: 30-03-2008",
            "SSC GPA: 3.78",
            "Currently studying at Shariatpur Government College (HSC Running)",
            "Profile is built around self-directed learning, freelance delivery, and real production projects rather than formal company employment history."
        ]),
        ("SECTION:Core Technical Skills", [
            "Laravel, PHP, JavaScript, Next.js, HTML, CSS, Tailwind CSS",
            "MySQL, REST API, API Integration, Payment Gateway Integration, SSLCommerz, Stripe, PayPal",
            "Facebook Pixel, Meta CAPI, Events API, Conversion API",
            "VPS Management, Linux, Docker, Git, GitHub, SEO, Admin Dashboard Development"
        ]),
        ("SECTION:Professional Experience", [
            "Freelance Full Stack Web Developer — independent client work and product builds.",
            "AI Assisted Software Developer — using AI-assisted workflows for faster implementation while verifying code quality and deployment readiness.",
            "Independent Client Projects — school and college management systems, e-commerce development, landing pages, and business automation systems.",
            "Real Client Work — live project delivery, API integration, payment setup, analytics tagging, and production deployment."
        ]),
        ("SECTION:Latest Work", [
            "Meta Tracking + Facebook Pixel + Conversions API + Events API",
            "Payment Gateway Integration and API Integration",
            "Production Deployment, Performance Optimization, and SEO improvements",
            "OfferLutBox.com and ZenFashions.shop as featured portfolio projects"
        ]),
        ("SECTION:Contact", [
            "Email: nobinmorsalin7@gmail.com",
            "WhatsApp: +880 1795-456495",
            "Portfolio: offerlutbox.com",
            "Experience Certificate / project documentation available on request"
        ])
    ]

    designer_sections = [
        ("SECTION:Professional Summary", [
            "Creative and product-focused full stack developer with a strong eye for premium UI, responsive experiences, and reliable engineering.",
            "Builds polished digital products using Laravel, PHP, JavaScript, Next.js, HTML, CSS, and Tailwind CSS with a strong focus on usability, accessibility, and performance.",
            "Works with AI-assisted development to accelerate implementation while keeping quality high for real-world deployment."
        ]),
        ("SECTION:Education & Background", [
            "Born: 30-03-2008",
            "SSC GPA: 3.78",
            "Currently studying at Shariatpur Government College (HSC Running)",
            "Experience is rooted in independent projects, freelance delivery, and production work rather than formal company employment history."
        ]),
        ("SECTION:Core Technical Skills", [
            "Frontend: HTML, CSS, JavaScript, Tailwind CSS, Next.js",
            "Backend: Laravel, PHP, REST API, API Integration, MySQL",
            "Growth & Marketing: Facebook Pixel, Meta CAPI, Events API, Conversion API, SEO",
            "Infrastructure: VPS Management, Linux, Docker, Git, GitHub, Payment Gateway Integration"
        ]),
        ("SECTION:Featured Projects", [
            "OfferLutBox.com — affiliate and offer management platform with analytics, smart redirects, and production deployment.",
            "ZenFashions.shop — modern e-commerce experience focused on responsive UI, product journeys, and fast performance.",
            "School & College Management Systems — admin dashboards, role-based workflows, records, and automation.",
            "Landing Pages and Business Automation Systems — conversion-focused websites and operational tools."
        ]),
        ("SECTION:Latest Work", [
            "Meta Tracking + Facebook Pixel + Conversions API + Events API",
            "Payment Gateway Integration using SSLCommerz, Stripe, and PayPal",
            "Production deployment, performance optimization, and SEO implementation",
            "AI-assisted development for rapid delivery across new stacks and frameworks"
        ]),
        ("SECTION:Contact", [
            "Email: nobinmorsalin7@gmail.com",
            "WhatsApp: +880 1795-456495",
            "Portfolio: offerlutbox.com",
            "Experience Certificate / project documentation available on request"
        ])
    ]

    Path("Nobin_Morsalin_ATS_Resume.pdf").write_bytes(build_pdf("Nobin Morsalin — ATS Resume", build_resume_pages("Nobin Morsalin — ATS Resume", ats_sections)))
    Path("Nobin_Morsalin_Designer_Resume.pdf").write_bytes(build_pdf("Nobin Morsalin — Designer Resume", build_resume_pages("Nobin Morsalin — Designer Resume", designer_sections)))
    print("Generated ATS and Designer resume PDFs.")


if __name__ == "__main__":
    main()
