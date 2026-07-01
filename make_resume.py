from pathlib import Path

PDF_TEMPLATE = b"""%PDF-1.4
%\xe2\xe3\xcf\xd3
"""


def pdf_escape(text: str) -> bytes:
    return (
        text
        .replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .encode("latin1", errors="replace")
    )


def build_page(content_lines):
    stream_lines = [b"BT /F1 12 Tf 50 780 Td"]
    for line in content_lines:
        escaped = pdf_escape(line)
        stream_lines.append(b"(" + escaped + b") Tj")
        stream_lines.append(b"T*")
    stream_lines.append(b"ET")
    stream = b"\n".join(stream_lines)
    return stream


def build_pdf(title, sections):
    content_lines = [title, ""]
    for heading, lines in sections:
        content_lines.append(heading)
        for line in lines:
            content_lines.append("  " + line)
        content_lines.append("")
    stream = build_page(content_lines)

    objects = []
    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    objects.append(
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n"
    )
    objects.append(
        b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    )
    objects.append(
        b"5 0 obj\n<< /Length %d >>\nstream\n%s\nendstream\nendobj\n"
        % (len(stream), stream)
    )

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


def main():
    ats_sections = [
        ("Professional Summary", [
            "AI-assisted full stack developer with a strong focus on production-ready",
            "web platforms, modern SaaS architecture, and scalable Laravel/Next.js systems.",
            "Experienced in analytics, affiliate offers, admin dashboards, and VPS deployment."
        ]),
        ("Core Skills", [
            "Laravel, PHP, Node.js, Next.js, React",
            "MySQL, PostgreSQL, Redis, Elasticsearch",
            "Docker, Nginx, Linux, VPS, CI/CD, GitHub Actions",
            "REST APIs, GraphQL, data pipelines, secure authentication"
        ]),
        ("Selected Achievements", [
            "Delivered OfferLutBox.com: affiliate tracking, smart redirects, analytics.",
            "Built school and college management systems with admin dashboards.",
            "Implemented 24/7 production deployments with Docker and VPS orchestration.",
            "Optimized application performance for multi-region traffic and SEO."
        ]),
        ("Professional Experience", [
            "Senior Full Stack Developer — freelance and product-focused clients.",
            "Led end-to-end development from concept to live production deployment.",
            "Integrated AI workflows for feature planning, code review and automation."
        ]),
        ("Education & Certifications", [
            "BSc in Computer Science (ongoing / self-taught modernization)",
            "Certified Laravel Developer / modern web and cloud delivery practices",
            "Professional training in UX, performance, and deployment security"
        ]),
        ("Contact", [
            "Email: nobinmorsalin7@gmail.com",
            "WhatsApp: +880 1795-456495",
            "Portfolio: offerlutbox.com"
        ]),
    ]

    designer_sections = [
        ("Designer CV Overview", [
            "Creative and functional front-end developer focused on premium product UX.",
            "Designs interfaces for SaaS, landing pages, dashboards, and business systems.",
            "Skilled at translating brand strategy into polished digital experiences."
        ]),
        ("Design Systems", [
            "Component-driven UI libraries, responsive layouts, and interaction patterns.",
            "Visual consistency across desktop, mobile, and tablet experiences.",
            "Modern typography, spacing, and color systems aligned with brand identity."
        ]),
        ("Project Highlights", [
            "OfferLutBox.com design system for conversion, analytics, and offer flows.",
            "Landing page and product UI for e-commerce, education, and business apps.",
            "Dashboard UX with metrics, workflows, and admin control panels."
        ]),
        ("Technical Design Skills", [
            "Figma, CSS3, Tailwind CSS, modern JavaScript, responsive components",
            "Animations, micro-interactions, and accessible web experiences",
            "Cross-browser compatibility, performance-aware styling, SEO-friendly markup"
        ]),
        ("Career Impact", [
            "Collaborated closely with founders and product teams to launch business tools.",
            "Delivered visual systems that improved engagement, clarity, and conversions.",
            "Balanced polished design with practical buildability and maintainability."
        ]),
        ("Contact", [
            "Email: nobinmorsalin7@gmail.com",
            "WhatsApp: +880 1795-456495",
            "Web: offerlutbox.com"
        ]),
    ]

    Path("Nobin_Morsalin_ATS_Resume.pdf").write_bytes(build_pdf("Nobin Morsalin — ATS Resume", ats_sections))
    Path("Nobin_Morsalin_Designer_Resume.pdf").write_bytes(build_pdf("Nobin Morsalin — Designer Resume", designer_sections))
    print("Generated ATS and Designer resume PDFs.")


if __name__ == "__main__":
    main()
