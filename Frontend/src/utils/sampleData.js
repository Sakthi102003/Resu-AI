// Sample resume data for different templates
export const getSampleResumeData = (templateId) => {
  const baseSample = {
    personal_info: {
      name: "Your Full Name",
      email: "your.email@example.com",
      phone: "+1-234-567-8900",
      location: "City, State, Country",
      linkedin: "linkedin.com/in/yourprofile",
      github: "github.com/yourusername",
      website: "yourwebsite.com"
    },
    summary: "Results-driven professional with X+ years of experience in [your field]. Proven expertise in [key skills] with a track record of [achievements]. Passionate about [your interests] and committed to delivering high-quality solutions.",
    experience: [
      {
        position: "Senior Software Engineer",
        company: "Tech Company Inc",
        location: "San Francisco, CA",
        start_date: "Jan 2022",
        end_date: "Present",
        current: true,
        description: [
          "Led development of microservices architecture serving 1M+ daily users",
          "Mentored team of 5 junior developers, improving code quality by 40%",
          "Implemented CI/CD pipeline reducing deployment time from 2hrs to 15min",
          "Collaborated with product team to define technical requirements"
        ]
      },
      {
        position: "Software Engineer",
        company: "Startup Solutions",
        location: "New York, NY",
        start_date: "Jun 2020",
        end_date: "Dec 2021",
        current: false,
        description: [
          "Built RESTful APIs using Python/Django and Node.js",
          "Designed and implemented database schemas for scalability",
          "Integrated third-party payment systems (Stripe, PayPal)",
          "Reduced API response time by 60% through optimization"
        ]
      },
      {
        position: "Junior Developer",
        company: "Digital Agency",
        location: "Austin, TX",
        start_date: "Jul 2018",
        end_date: "May 2020",
        current: false,
        description: [
          "Developed responsive web applications using React and Vue.js",
          "Fixed bugs and implemented new features based on client feedback",
          "Participated in agile development process and daily standups"
        ]
      }
    ],
    education: [
      {
        degree: "Master of Science",
        field_of_study: "Computer Science",
        institution: "Stanford University",
        location: "Stanford, CA",
        start_date: "2016",
        end_date: "2018",
        graduation_date: "May 2018",
        gpa: "3.9/4.0",
        description: "Coursework: Machine Learning, Distributed Systems, Algorithms"
      },
      {
        degree: "Bachelor of Science",
        field_of_study: "Computer Science",
        institution: "University of California, Berkeley",
        location: "Berkeley, CA",
        start_date: "2012",
        end_date: "2016",
        graduation_date: "May 2016",
        gpa: "3.7/4.0",
        description: "Honors: Dean's List, Cum Laude"
      }
    ],
    skills: [
      {
        category: "Languages",
        items: ["Python", "JavaScript", "TypeScript", "Java", "C++", "SQL", "Go"]
      },
      {
        category: "Frontend",
        items: ["React", "Vue.js", "Angular", "HTML5", "CSS3", "Tailwind CSS"]
      },
      {
        category: "Backend",
        items: ["Node.js", "Django", "FastAPI", "Express", "Spring Boot"]
      },
      {
        category: "Databases",
        items: ["PostgreSQL", "MongoDB", "Redis", "MySQL", "DynamoDB"]
      },
      {
        category: "DevOps",
        items: ["Docker", "Kubernetes", "AWS", "GCP", "Jenkins", "GitHub Actions"]
      },
      {
        category: "Tools",
        items: ["Git", "VS Code", "Postman", "Figma", "Jira", "Slack"]
      }
    ],
    projects: [
      {
        name: "E-Commerce Platform",
        description: "Full-stack marketplace with real-time inventory management and payment processing. Handles 10K+ transactions/month with 99.9% uptime.",
        technologies: ["React", "Node.js", "PostgreSQL", "Stripe API", "AWS"],
        url: "github.com/yourusername/ecommerce-platform",
        start_date: "2023",
        end_date: "2023"
      },
      {
        name: "AI-Powered Chat Application",
        description: "Real-time chat app with AI-powered message suggestions and sentiment analysis. 5K+ active users with real-time message processing.",
        technologies: ["React", "FastAPI", "OpenAI API", "WebSocket", "MongoDB"],
        url: "github.com/yourusername/ai-chat",
        start_date: "2023",
        end_date: "2023"
      },
      {
        name: "Portfolio Analytics Dashboard",
        description: "Interactive dashboard for tracking investment portfolio performance. Real-time data visualization with custom analytics engine.",
        technologies: ["Vue.js", "Python", "D3.js", "PostgreSQL"],
        url: "yourwebsite.com/portfolio",
        start_date: "2022",
        end_date: "2022"
      }
    ],
    certifications: [
      {
        name: "AWS Certified Solutions Architect - Associate",
        issuer: "Amazon Web Services",
        date: "2023"
      },
      {
        name: "Professional Scrum Master I (PSM I)",
        issuer: "Scrum.org",
        date: "2023"
      },
      {
        name: "MongoDB Certified Developer",
        issuer: "MongoDB University",
        date: "2022"
      }
    ],
    awards: [
      "Best Innovation Award - Company Hackathon 2023",
      "Dean's List - All 4 years",
      "Academic Scholarship - University Name 2022"
    ],
    languages: [
      "English (Native)",
      "Spanish (Professional Working Proficiency)",
      "French (Elementary Proficiency)"
    ]
  };

  // Customize based on template
  const templateSpecificData = {
    auto_cv: baseSample,
    anti_cv: {
      ...baseSample,
      summary: "This is an Anti-CV highlighting professional growth, lessons learned from failures, and continuous improvement. Every rejection and setback has been a stepping stone to success."
    },
    ethan: baseSample,
    rendercv_classic: baseSample,
    rendercv_engineering: {
      ...baseSample,
      summary: "Senior Software Engineer with expertise in system design, algorithms, and scalable architecture. Strong foundation in computer science principles with proven ability to deliver high-performance solutions."
    },
    rendercv_sb2nov: baseSample,
    yuan: {
      ...baseSample,
      summary: "Research-oriented professional with focus on innovation and academic excellence. Published researcher with strong analytical and problem-solving skills."
    }
  };

  return templateSpecificData[templateId] || baseSample;
};
