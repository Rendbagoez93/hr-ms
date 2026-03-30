# HTML Template Development Standards

This document outlines the standards and best practices for creating HTML templates within the HR-MS Django project. Adherence to these guidelines is mandatory to ensure consistency, accessibility, SEO performance, and maintainability across all web pages.

---

## 1. Language

-   **UI Text**: All user-facing text content should be Bilingual **English**, **Indonesian (Bahasa Indonesia)**.
-   **Code & Comments**: All template code, including variable names, block names, template tags, and comments, must be in **English**.

```html
<!-- Good -->
<h1>Detail Karyawan</h1>
<p>{{ employee.name }}</p>

<!-- Bad -->
<h1>Employee Details</h1>
<p>{{ karyawan.nama }}</p>
```

---

## 2. Template Structure

Templates must follow a consistent structure to promote reusability and separation of concerns.

### File Organization

-   **Layouts (`templates/layouts/`)**: Base templates that define the main page structure (e.g., `base.html`, `auth_base.html`).
-   **Pages (`templates/pages/`)**: Full-page templates that extend a layout. Each page should correspond to a specific URL.
-   **Partials (`templates/partials/`)**: Reusable template fragments (e.g., `_header.html`, `_footer.html`, `_form_field.html`). Partial filenames must be prefixed with an underscore (`_`).

### Required Blocks in `base.html`

Every page template must extend a base layout and define the following blocks:

-   `{% block title %}`: For the page title (`<title>` tag).
-   `{% block meta %}`: For page-specific meta tags (description, keywords, Open Graph).
-   `{% block styles %}`: For page-specific CSS files.
-   `{% block content %}`: The main content of the page.
-   `{% block scripts %}`: For page-specific JavaScript files or inline scripts.

```html
<!-- templates/layouts/base.html -->
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}HR-MS{% endblock %}</title>
    {% block meta %}{% endblock %}
    {% block styles %}{% endblock %}
</head>
<body>
    {% include "partials/_header.html" %}
    <main>
        {% block content %}{% endblock %}
    </main>
    {% include "partials/_footer.html" %}
    {% block scripts %}{% endblock %}
</body>
</html>
```

---

## 3. SEO Rules

-   **Title Tag**: Every page must have a unique, descriptive title (60 characters max). Format: `[Page Title] | [Site Name]`.
-   **Meta Description**: Provide a concise summary of the page's content (160 characters max).
-   **Structured Data**: Use JSON-LD for structured data where appropriate (e.g., articles, events).
-   **Heading Hierarchy**:
    -   Each page must have exactly one `<h1>` tag.
    -   Maintain a logical heading order (`<h1>` -> `<h2>` -> `<h3>`). Do not skip levels.
-   **Open Graph & Twitter Cards**: Include `og:` and `twitter:` meta tags for social sharing.

---

## 4. Semantic HTML

Use HTML5 elements according to their semantic meaning to improve accessibility and SEO.

-   `<header>`: For introductory content or navigational links.
-   `<footer>`: For the footer of a page or section.
-   `<main>`: For the primary content of the page.
-   `<nav>`: For major navigation blocks.
-   `<article>`: For self-contained content (e.g., a blog post).
-   `<section>`: For thematic groupings of content.
-   `<aside>`: For content tangentially related to the main content (e.g., a sidebar).

---

## 5. CSS Rules

-   **No Inline Styles**: Never use the `style` attribute. All styles must be in external CSS files.
-   **Design Tokens**: Use CSS variables (design tokens) for colors, fonts, and spacing to ensure consistency.
-   **Utility-First**: Prefer using utility classes (when a framework like Tailwind CSS is integrated). Custom CSS should be minimal.
-   **BEM Naming**: For custom components, use the Block-Element-Modifier (BEM) naming convention.

---

## 6. JavaScript Rules

-   **HTMX**: Use HTMX for server-driven partial page updates. This is the primary method for creating dynamic interfaces.
-   **Alpine.js**: Use Alpine.js for small, client-side interactions (e.g., toggling modals, dropdowns, tabs).
-   **Vanilla JS**: For complex logic not covered by HTMX/Alpine, write modern, modular Vanilla JavaScript (ES6+). Avoid jQuery.
-   **Script Placement**: Place scripts at the end of the `<body>` tag within the `{% block scripts %}` block, unless a script must be in the `<head>`.

---

## 7. Django 6.0 Partials

-   **`{% include %}`**: Use `{% include "partials/_my_partial.html" %}` for reusable UI components.
-   **`{% include ... with ... %}`**: Pass context variables to partials explicitly. Avoid relying on the parent context.

```html
<!-- Good: Explicit context passing -->
{% include "partials/_user_card.html" with user=employee.user %}

<!-- Bad: Implicit context reliance -->
{% include "partials/_user_card.html" %}
```

---

## 8. Accessibility (WCAG 2.1 AA)

-   **Image `alt` Attributes**: All `<img>` tags must have a descriptive `alt` attribute. For decorative images, use `alt=""`.
-   **Form Labels**: All form inputs must have an associated `<label>`.
-   **Keyboard Navigation**: All interactive elements must be focusable and operable via keyboard.
-   **Color Contrast**: Ensure text and background colors have sufficient contrast ratio.

---

## 9. No-Emoji Rule

Do not use emojis directly in templates or UI copy. Instead, use an icon library (e.g., Font Awesome, Bootstrap Icons) for iconography to ensure consistent rendering and professional appearance.

---

## 10. File Naming Conventions

-   **Templates**: `snake_case.html` (e.g., `employee_detail.html`).
-   **Partials**: `_snake_case.html` (e.g., `_employee_form.html`).
-   **CSS**: `kebab-case.css` (e.g., `employee-styles.css`).
-   **JavaScript**: `kebab-case.js` (e.g., `employee-scripts.js`).

---

## 11. Adding a New Public Page — Checklist

Follow these steps to add a new page to the website.

1.  [ ] **Create View**: Create a new Django class-based view in the appropriate `views.py`.
2.  [ ] **Create URL Route**: Add a new URL pattern in the appropriate `urls.py`.
3.  [ ] **Create Template File**: Create a new HTML template in `templates/pages/`.
4.  [ ] **Extend Base Layout**: The new template must extend `layouts/base.html` or another suitable base layout.
5.  [ ] **Define Title Block**: Add a unique and descriptive `{% block title %}`.
6.  [ ] **Define Meta Block**: Add a `{% block meta %}` with a meta description.
7.  [ ] **Add Content**: Implement the page content within the `{% block content %}` using semantic HTML.
8.  [ ] **Check Heading Structure**: Ensure there is one `<h1>` and a logical heading hierarchy.
9.  [ ] **Add Partials**: Use existing partials for common elements like forms or cards.
10. [ ] **Check Accessibility**: Verify form labels, image alt tags, and keyboard navigation.
11. [ ] **Test**: Manually test the page on different screen sizes and browsers.
