#!/usr/bin/env python3
"""Complete CV generator with all technical + design content."""
from pathlib import Path
from typing import List, Tuple

class SimplePDF:
    def __init__(self):
        self.pages = []
        
    def add_text_page(self, title: str, sections: List[Tuple[str, List[str]]]) -> None:
        """Add a page with title and sections of text."""
        content = f"{title}\n" + "=" * 70 + "\n\n"
        
        for section_title, lines in sections:
            content += f"\n{section_title}\n" + "-" * len(section_title) + "\n"
            for line in lines:
                while len(line) > 95:
                    idx = line.rfind(" ", 0, 95)
                    if idx == -1:
                        idx = 95
                    content += line[:idx] + "\n"
                    line = line[idx:].lstrip()
                content += line + "\n"
            content += "\n"
        
        self.pages.append(content)
    
    def build_pdf(self) -> bytes:
        """Build a PDF with all pages."""
        pdf_objects = []
        pdf_objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
        
        page_refs = " ".join([f"{3 + i} 0 R" for i in range(len(self.pages))])
        pdf_objects.append(
            f"2 0 obj\n<< /Type /Pages /Kids [{page_refs}] /Count {len(self.pages)} >>\nendobj\n".encode()
        )
        
        for i, page_text in enumerate(self.pages):
            stream = self._create_stream(page_text)
            obj_num = 3 + i
            content_obj_num = 3 + len(self.pages) + i
            
            page_obj = (
                f"{obj_num} 0 obj\n"
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                f"/Resources << /Font << /F1 {3 + len(self.pages) * 2} 0 R >> >> "
                f"/Contents {content_obj_num} 0 R >>\nendobj\n"
            ).encode()
            pdf_objects.append(page_obj)
        
        for i, page_text in enumerate(self.pages):
            stream = self._create_stream(page_text)
            obj_num = 3 + len(self.pages) + i
            pdf_objects.append(
                f"{obj_num} 0 obj\n<< /Length {len(stream)} >>\nstream\n".encode() +
                stream +
                b"\nendstream\nendobj\n"
            )
        
        font_obj_num = 3 + len(self.pages) * 2
        pdf_objects.append(
            f"{font_obj_num} 0 obj\n"
            f"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>\nendobj\n".encode()
        )
        
        output = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
        xref_offsets = [len(output)]
        
        for obj in pdf_objects:
            xref_offsets.append(len(output))
            output += obj
        
        xref_start = len(output)
        output += b"xref\n"
        output += f"0 {len(xref_offsets)}\n".encode()
        output += b"0000000000 65535 f \n"
        for offset in xref_offsets[:-1]:
            output += f"{offset:010d} 00000 n \n".encode()
        
        output += b"trailer\n"
        output += f"<< /Size {len(xref_offsets)} /Root 1 0 R >>\n".encode()
        output += b"startxref\n"
        output += f"{xref_start}\n".encode()
        output += b"%%EOF\n"
        
        return output
    
    def _create_stream(self, text: str) -> bytes:
        """Create a PDF text stream."""
        lines = text.split("\n")
        stream = b"BT /F1 10 Tf 50 800 Td\n"
        
        for line in lines:
            if line == "\f":
                stream += b"ET\nET\n"
                continue
            
            safe_line = (
                line.replace("\\", "\\\\")
                    .replace("(", "\\(")
                    .replace(")", "\\)")
            )
            
            if safe_line.strip():
                stream += f"({safe_line}) Tj\n".encode()
            stream += b"0 -14 Td\n"
        
        stream += b"ET\n"
        return stream


# Designer Resume - COMPLETE with all technical + design sections
DESIGNER_PAGE_1 = [
    ("NOBIN MORSALIN", [
        "Full Stack Developer & Premium UI/UX Designer",
        "Building beautiful, performant, and accessible digital experiences",
        "",
        "Email: nobinmorsalin7@gmail.com | WhatsApp: +8801795456495",
        "Location: Damudya, Shariatpur, Bangladesh | Portfolio: offerlutbox.com",
    ]),
    ("PROFESSIONAL SUMMARY", [
        "Creative Full Stack Developer and UI/UX Designer with 3+ years building premium digital",
        "products that combine stunning visuals with robust engineering. Specialized in design systems,",
        "responsive interfaces, and high-performance applications using React, Next.js, Laravel, and",
        "Tailwind CSS. Fluent in design tools (Figma) and modern web development. Passionate about",
        "accessibility, performance, and user-centered design. Expert in AI-assisted development.",
    ]),
    ("CAREER OBJECTIVE", [
        "Seeking Creative Developer or Senior UI/UX role to lead design-driven product development,",
        "build scalable design systems, mentor teams on accessibility, and create inclusive experiences.",
        "Committed to building beautiful interfaces that are both functional and high-performing.",
    ]),
    ("TECHNICAL SKILLS - FRONTEND", [
        "HTML5: Semantic markup, accessibility, progressive enhancement, proper structure",
        "",
        "CSS3: Flexbox, CSS Grid, custom properties, animations, transitions, responsive units",
        "",
        "JavaScript: ES6+, DOM manipulation, event handling, async/await, interactive components",
        "",
        "React: Component architecture, hooks, state management, performance optimization",
        "",
        "Next.js: Server-side rendering, static generation, image optimization, API routes",
        "",
        "Tailwind CSS: Utility-first workflow, component composition, custom theming, dark mode",
        "",
        "AJAX & REST APIs: JSON consumption, async data loading, error handling, WebSockets",
    ]),
    ("TECHNICAL SKILLS - BACKEND & INFRASTRUCTURE", [
        "PHP: Object-oriented programming, design patterns, best practices",
        "",
        "Laravel: MVC architecture, Eloquent ORM, migrations, authentication, routing, middleware",
        "",
        "Node.js & Express: RESTful API development, middleware, error handling, request routing",
        "",
        "MySQL: Database design, optimization, indexing, query tuning, migrations, relationships",
        "",
        "PostgreSQL: Advanced queries, JSON support, relationships, performance optimization",
        "",
        "Redis: Caching, queue systems, session storage, real-time data handling, pub/sub",
        "",
        "Docker: Containerization, multi-container apps, production deployments, scaling",
        "",
        "Linux & VPS: Server management, Nginx, Apache, SSL certificates, deployment automation",
        "",
        "Git & GitHub: Version control, branching, pull requests, collaborative workflows",
    ]),
]

DESIGNER_PAGE_2 = [
    ("DESIGN EXPERTISE", [
        "Visual Design: Color theory, typography, spacing systems, icon design, brand systems",
        "",
        "UI Components: Buttons, forms, navigation, modals, cards, data tables, complex layouts",
        "",
        "Interaction Design: Micro-interactions, transitions, animations, feedback, hover states",
        "",
        "UX Principles: User research, wireframing, prototyping, usability testing, accessibility",
        "",
        "Responsive Design: Mobile-first approach, adaptive layouts, breakpoint strategy",
        "",
        "Design Systems: Component libraries, design tokens, documentation, consistency at scale",
        "",
        "Tools: Figma (expert), Adobe XD, CSS animations, prototyping, handoff documentation",
    ]),
    ("SPECIALIZED COMPETENCIES", [
        "SEO & Technical SEO: Meta tags, structured data, Core Web Vitals, performance metrics",
        "",
        "Performance Optimization: Code splitting, lazy loading, critical CSS, image optimization",
        "",
        "Responsive Web Design: Mobile-first, flexible grids, breakpoint strategy, touch-friendly",
        "",
        "UI/UX Understanding: User psychology, interaction patterns, accessibility (WCAG 2.1 AA)",
        "",
        "AI-Assisted Development: GitHub Copilot, ChatGPT, Claude for code generation, workflows",
        "",
        "Flutter (Basic): Mobile app development, widget architecture, state management",
    ]),
    ("FEATURED PROJECTS - OfferLutBox.com", [
        "Complete Product Design + Full Stack Development",
        "",
        "Description: Premium SaaS affiliate platform with design system and technical foundation.",
        "",
        "DESIGN WORK:",
        "  - Designed 50+ reusable UI components in comprehensive design system",
        "  - Intuitive dashboard UI for affiliate marketers with real-time analytics",
        "  - Responsive layouts: desktop, tablet, mobile with touch optimization",
        "  - Micro-interactions and smooth animations throughout user experience",
        "  - WCAG 2.1 AA accessibility compliance, keyboard navigation, screen reader support",
        "  - Performance optimizations: critical CSS, image optimization, lazy loading",
        "",
        "TECHNICAL IMPLEMENTATION:",
        "  - Backend: Laravel 10 with 50+ RESTful API endpoints for offer management",
        "  - Frontend: React + Next.js dashboard with real-time data updates",
        "  - Database: PostgreSQL with optimized schemas for tracking and analytics",
        "  - Caching: Redis for high-volume conversion data and queue management",
        "  - Deployment: Docker containers on Linux VPS with Nginx and SSL",
        "",
        "Results: 99.5% uptime, 94 Lighthouse score, 100K+ daily conversions, 150+ users",
    ]),
    ("FEATURED PROJECTS - E-Commerce & School Systems", [
        "Multi-Project Experience",
        "",
        "E-Commerce Platform: Multi-vendor marketplace with design system, product UI, admin",
        "  dashboards, payment integration (Stripe/SSL Commerz/bKash), inventory, analytics.",
        "",
        "School Management System: Complete digital transformation with role-based dashboards",
        "  (admin/teacher/student/parent), attendance, exams, fees, reports. Deployed 5+ schools.",
        "",
        "College Management System: Online admission, course registration, fee tracking, exams,",
        "  communication system, transcript generation. Built with Laravel, PostgreSQL, Vue.js.",
    ]),
]

DESIGNER_PAGE_3 = [
    ("DESIGN SYSTEM COMPONENTS", [
        "Comprehensive Component Library (50+ components) for OfferLutBox.com",
        "",
        "FOUNDATIONAL ELEMENTS:",
        "  Buttons (primary/secondary/ghost states), Form controls (inputs/selects/toggles)",
        "  Cards (standard/expandable with hover effects), Navigation (sidebar/breadcrumbs/tabs)",
        "",
        "DATA DISPLAY:",
        "  Tables (sortable/filterable), Charts (line/bar/pie), Metrics (KPI cards/trends)",
        "  Alerts (info/success/warning/error), Progress indicators, Status badges",
        "",
        "INTERACTIONS:",
        "  Modals with focus management, Tooltips with smart positioning",
        "  Dropdowns with keyboard nav, Loading states with skeleton screens",
        "  Empty states with illustrations, Toast notifications with auto-dismiss",
        "",
        "ACCESSIBILITY:",
        "  Keyboard navigation, ARIA labels, WCAG AA color contrast, Focus indicators",
        "  Screen reader optimization, Semantic HTML, Proper heading hierarchy",
    ]),
    ("EDUCATION & PROFESSIONAL DEVELOPMENT", [
        "Current: Shariatpur Government College, Bangladesh",
        "  Self-directed learning in modern web design and development",
        "",
        "Secondary: SSC (GPA: 3.78) - Shariatpur Government School",
        "",
        "Professional Training & Certifications:",
        "  - Figma Advanced: Design systems, prototyping, collaboration, handoff workflows",
        "  - Web Design Fundamentals: UX principles, accessibility, responsive design patterns",
        "  - CSS Mastery: Animations, transitions, modern layout, performance techniques",
        "  - JavaScript Advanced: DOM, ES6+, async, event handling, interactive components",
        "  - React & Next.js: Components, hooks, SSR, static generation, performance",
        "  - Laravel Backend: MVC, database design, API development, authentication",
        "  - Accessibility: WCAG 2.1, ARIA, inclusive design, assistive technology",
        "",
        "Self-Taught Expertise:",
        "  UI/UX design psychology, performance optimization, Docker deployment,",
        "  Technical SEO, AI-assisted development workflows, design systems at scale",
    ]),
    ("PERSONAL INFORMATION", [
        "Full Name: Nobin Morsalin | Gender: Male | Nationality: Bangladeshi",
        "",
        "Father's Name: Nasir Sikder",
        "Mother's Name: Ferdousi Begum",
        "",
        "Permanent Address: Purbakandi, Damudya, Shariatpur, Bangladesh",
        "Present Address: Same as Permanent Address",
        "",
        "CONTACT:",
        "  Email: nobinmorsalin7@gmail.com",
        "  WhatsApp: +8801795456495",
        "  Portfolio & Live Projects: offerlutbox.com",
    ]),
    ("ADDITIONAL COMPETENCIES", [
        "Problem-Solving: Strong analytical and debugging skills, creative solutions",
        "",
        "Communication: Technical writing, client presentations, team collaboration",
        "",
        "Teamwork: Collaborative projects, peer code review, mentoring, knowledge sharing",
        "",
        "Time Management: On-time delivery, agile methodology, sprint planning, priorities",
        "",
        "Adaptability: Quick learner for new technologies, frameworks, design tools",
        "",
        "AI Workflows: GitHub Copilot, ChatGPT, Claude for productivity + quality maintenance",
        "",
        "Languages: Bengali (Native/Fluent), English (Professional), Hindi (Basic)",
    ]),
]

def generate_pdfs():
    """Generate both ATS and Designer CVs."""
    
    # ATS Resume (comprehensive version)
    ats_sections_p1 = [
        ("NOBIN MORSALIN - ATS RESUME", [
            "Full Stack Web Developer | Laravel | Next.js | AI-Assisted Engineering",
            "Email: nobinmorsalin7@gmail.com | WhatsApp: +8801795456495",
            "Location: Damudya, Shariatpur, Bangladesh",
        ]),
        ("PROFESSIONAL SUMMARY", [
            "Results-driven Full Stack Developer, 3+ years experience building production-ready",
            "web applications, scalable SaaS platforms, enterprise admin systems. Specialized in",
            "Laravel backend, Next.js frontend, MySQL optimization, Docker VPS deployment.",
            "Experienced in AI-assisted development workflows (GitHub Copilot, ChatGPT, Claude).",
            "Proven ability: concept to production deployment, clean code, REST API design,",
            "performance optimization, sustainable development practices on Linux/VPS.",
        ]),
        ("CAREER OBJECTIVE", [
            "Seeking Senior Full Stack Developer/Lead Engineer role to leverage expertise in",
            "modern web architectures, AI development, and cloud deployment. Building scalable,",
            "high-performance applications with measurable business impact.",
        ]),
        ("CORE COMPETENCIES", [
            "Backend: Laravel, PHP, Node.js, Express, REST APIs, GraphQL basics",
            "Frontend: React, Next.js, JavaScript ES6+, HTML5, CSS3, Tailwind CSS, AJAX",
            "Database: MySQL, PostgreSQL, Redis caching, optimization, design patterns",
            "DevOps: Linux, Nginx, Apache, Docker, VPS, CI/CD, GitHub Actions",
            "Tools: Git, GitHub, Composer, NPM/Yarn, Figma, VS Code, AI assistants",
            "Specializations: SEO, performance tuning, responsive design, UI/UX",
            "AI & Automation: GitHub Copilot, ChatGPT, Claude, workflow automation",
        ]),
        ("TECHNICAL SKILLS", [
            "Languages: PHP, JavaScript, HTML5, CSS3, SQL, Bash, Basic Flutter",
            "Backends: Laravel (8-11), Express.js, Node.js patterns",
            "Frontend: React, Next.js, Tailwind CSS, component design",
            "Databases: MySQL, PostgreSQL, Redis caching, optimization, indexing",
            "Web Tech: REST APIs, JSON, XML, AJAX, WebSockets, OAuth 2.0",
            "DevOps: Docker, Linux (Ubuntu/CentOS), Nginx, Apache, VPS mgmt",
            "Version Control: Git, GitHub, branching, pull request workflows",
            "Tools: WordPress, Figma, VS Code, PhpStorm",
            "SEO & Performance: Technical SEO, speed optimization, Core Web Vitals",
            "AI Tools: Copilot, ChatGPT, Claude, Gemini for development",
        ]),
        ("PROFESSIONAL EXPERIENCE", [
            "FREELANCE FULL STACK DEVELOPER (2023-Present)",
            "",
            "OfferLutBox.com: Affiliate platform with Laravel backend, React+Next.js frontend,",
            "  PostgreSQL, Redis, Docker deployment. 50+ API endpoints, real-time analytics.",
            "",
            "E-Commerce Platforms: Product management, inventory, payment integration",
            "  (SSL Commerz, bKash, Stripe), order management, analytics.",
            "",
            "School Management System: Student records, attendance, exams, fees, parent portal,",
            "  Laravel+Bootstrap. Deployed 5+ schools, 1000+ students.",
            "",
            "College Management System: Admission, course registration, fees, exams, communication.",
            "",
            "API Architecture: Mobile-app support, third-party integrations, microservices.",
            "",
            "Production Deployment: 10+ apps on DigitalOcean/Linode using Docker, Nginx, SSL.",
            "  Zero-downtime deployments, auto-scaling, monitoring.",
            "",
            "AI Workflow Integration: GitHub Copilot, ChatGPT, Claude for 40%+ dev acceleration",
            "  with code quality maintained through manual review.",
        ]),
    ]
    
    ats_sections_p2 = [
        ("FEATURED PROJECTS", [
            "OfferLutBox.com - Affiliate & Offer Management SaaS",
            "",
            "Technologies: Laravel 10, React, Next.js, PostgreSQL, Redis, Docker, Nginx",
            "",
            "Responsibilities:",
            "  - 50+ RESTful API endpoints for offer, tracking, analytics management",
            "  - React dashboard with real-time analytics, WebSockets, Redis pub/sub",
            "  - Affiliate tracking: pixel tracking, postback handling, multi-network support",
            "  - Landing page builder with drag-drop, templates, SEO optimization",
            "  - Database schema for offers, conversions, affiliates, normalized structure",
            "",
            "Challenges & Solutions:",
            "  - High-volume tracking: Redis queue + batch processing with Laravel Horizon",
            "  - Multi-network complexity: Abstraction layer for network-specific APIs",
            "",
            "Results: 99.5% uptime, 100K+ daily conversions, 150+ affiliate accounts",
            "",
            "",
            "E-Commerce Platform with Multi-Vendor Support",
            "",
            "Technologies: Laravel, MySQL, Tailwind CSS, Stripe/SSL Commerz, AWS S3",
            "",
            "Features: Multi-vendor marketplace, commission management, product catalog,",
            "  advanced filtering, secure payments, order management, invoice generation,",
            "  shipment tracking, admin analytics, customer reviews, rating system",
            "",
            "Achievements: 60% page load time reduction via query optimization, image",
            "  optimization with WebP, PDF invoice generation, payment retry logic",
            "",
            "",
            "School Management System",
            "",
            "Technologies: Laravel, MySQL, Bootstrap 5, jQuery, Google Charts",
            "",
            "Features: Student management, registration, class management, attendance",
            "  with SMS notifications, exam management (questions, marking, results),",
            "  fee collection, teacher dashboard, parent portal, admin reporting",
            "",
            "Impact: 5+ schools, 1000+ students managed",
            "",
            "",
            "College Management System",
            "",
            "Technologies: Laravel, PostgreSQL, Vue.js, REST API",
            "",
            "Features: Online admission, course registration, prerequisites, fees, exams,",
            "  communication system, transcripts, degree verification",
        ]),
        ("EDUCATION", [
            "Running Student: Shariatpur Government College, Bangladesh",
            "  Self-directed modern web tech and cloud deployment learning",
            "",
            "Secondary Education: SSC (GPA: 3.78)",
            "  Shariatpur Government School",
            "",
            "Self-Education & Certs: Complete Laravel, Advanced JavaScript/React, Docker,",
            "  AWS & DigitalOcean deployment, DevOps, CI/CD",
        ]),
        ("PERSONAL INFORMATION", [
            "Full Name: Nobin Morsalin | Gender: Male | Nationality: Bangladeshi",
            "",
            "Father: Nasir Sikder | Mother: Ferdousi Begum",
            "",
            "Permanent: Purbakandi, Damudya, Shariatpur, Bangladesh",
            "Present: Same",
            "",
            "Email: nobinmorsalin7@gmail.com",
            "WhatsApp: +8801795456495",
            "Portfolio: offerlutbox.com",
        ]),
        ("LANGUAGES", [
            "Bengali: Native/Fluent",
            "English: Professional working",
            "Hindi: Basic conversational",
        ]),
        ("ADDITIONAL SKILLS", [
            "Problem-solving: Analytical, debugging, creative solutions",
            "Communication: Technical writing, client interaction",
            "Teamwork: Collaborative, code review, peer support",
            "Time Management: On-time delivery, agile practices",
            "Adaptability: Quick learner for new tech and frameworks",
            "AI Integration: Copilot, ChatGPT, Claude for productivity",
        ]),
    ]
    
    print("Generating ATS Resume...")
    ats_pdf = SimplePDF()
    ats_pdf.add_text_page("NOBIN MORSALIN - ATS RESUME PAGE 1", ats_sections_p1)
    ats_pdf.add_text_page("NOBIN MORSALIN - ATS RESUME PAGE 2", ats_sections_p2)
    ats_output = Path("Nobin_Morsalin_ATS_Resume.pdf")
    ats_output.write_bytes(ats_pdf.build_pdf())
    print(f"✓ ATS Resume: {ats_output.stat().st_size} bytes, {len(ats_pdf.pages)} pages")
    
    # Designer Resume (NEW COMPLETE VERSION)
    print("Generating Designer Resume...")
    designer_pdf = SimplePDF()
    designer_pdf.add_text_page("NOBIN MORSALIN - DESIGNER RESUME PAGE 1", DESIGNER_PAGE_1)
    designer_pdf.add_text_page("NOBIN MORSALIN - DESIGNER RESUME PAGE 2", DESIGNER_PAGE_2)
    designer_pdf.add_text_page("NOBIN MORSALIN - DESIGNER RESUME PAGE 3", DESIGNER_PAGE_3)
    designer_output = Path("Nobin_Morsalin_Designer_Resume.pdf")
    designer_output.write_bytes(designer_pdf.build_pdf())
    print(f"✓ Designer Resume: {designer_output.stat().st_size} bytes, {len(designer_pdf.pages)} pages")
    
    return ats_output, designer_output

if __name__ == "__main__":
    ats_file, designer_file = generate_pdfs()
    print(f"\n✅ CVs regenerated with complete content!")
