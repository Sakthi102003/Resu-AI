# 🎨 Template Panel - Visual Guide

## Layout Overview

```
┌─────────────────────────────────────────────────────────────┐
│  LaTeX Editor Layout                                        │
├─────────────┬─────────────────┬──────────────────────────┐  │
│   Code      │   PDF Preview   │   TEMPLATE PANEL        │  │
│   Editor    │                 │   (320px wide)          │  │
│             │                 │   [OVERSHADOWS OTHER]   │  │
│             │                 │                         │  │
│             │                 │  ┌──────────────────┐   │  │
│             │                 │  │ 🎨 HEADER        │   │  │
│             │                 │  │ Gradient Header  │   │  │
│             │                 │  └──────────────────┘   │  │
│             │                 │                         │  │
│             │                 │  ┌──────────────────┐   │  │
│             │                 │  │ 📄 Templates (7) │   │  │
│             │                 │  ├──────────────────┤   │  │
│             │                 │  │ 🤖 Auto CV       │   │  │
│             │                 │  │ 🎨 Anti CV       │   │  │
│             │                 │  │ 💼 Ethan's       │   │  │
│             │                 │  │ 🎓 Classic       │   │  │
│             │                 │  │ ⚙️ Engineering   │   │  │
│             │                 │  │ 💻 sb2nov        │   │  │
│             │                 │  │ ✨ Yuan's        │   │  │
│             │                 │  └──────────────────┘   │  │
│             │                 │                         │  │
│             │                 │  ┌──────────────────┐   │  │
│             │                 │  │ 🎨 Colors (8)    │   │  │
│             │                 │  ├──────────────────┤   │  │
│             │                 │  │ 💼 Blue          │   │  │
│             │                 │  │ 🌿 Green         │   │  │
│             │                 │  │ 🎨 Purple        │   │  │
│             │                 │  │ 🔥 Red           │   │  │
│             │                 │  │ 🌟 Orange        │   │  │
│             │                 │  │ 💎 Teal          │   │  │
│             │                 │  │ 🌸 Pink          │   │  │
│             │                 │  │ 👔 Indigo        │   │  │
│             │                 │  └──────────────────┘   │  │
│             │                 │                         │  │
│             │                 │  ┌──────────────────┐   │  │
│             │                 │  │ FOOTER           │   │  │
│             │                 │  │ Current Selection│   │  │
│             │                 │  └──────────────────┘   │  │
└─────────────┴─────────────────┴──────────────────────────┘  │
```

## Panel Sections

### 1️⃣ HEADER (Gradient: Primary → Purple)
```
╔══════════════════════════════════════╗
║  [X]                                 ║
║  📄 Customize Resume                 ║
║  Choose your perfect style           ║
╚══════════════════════════════════════╝
```
- White text on gradient background
- Collapse button (X) in top-right
- Icon + Title + Subtitle

### 2️⃣ TEMPLATES SECTION
```
╔══════════════════════════════════════╗
║  📄 Templates (7)              [▼]   ║
╠══════════════════════════════════════╣
║                                      ║
║  ┌────────────────────────────────┐  ║
║  │ 🤖 Auto CV              [✓]    │  ║
║  │ Modern, automated, ATS-friendly│  ║
║  │ [Modern] [✓ ATS]               │  ║
║  └────────────────────────────────┘  ║
║                                      ║
║  ┌────────────────────────────────┐  ║
║  │ 🎨 Anti CV                     │  ║
║  │ Creative, story-driven format  │  ║
║  │ [Creative]                     │  ║
║  └────────────────────────────────┘  ║
║                                      ║
║  ... (5 more templates)              ║
║                                      ║
╚══════════════════════════════════════╝
```

**Template Card States:**
- **Default**: White background, gray border
- **Hover**: Scale 1.02x, subtle shadow
- **Selected**: Gradient background, checkmark icon, colored border

### 3️⃣ COLORS SECTION
```
╔══════════════════════════════════════╗
║  🎨 Theme Colors (8)           [▼]   ║
╠══════════════════════════════════════╣
║                                      ║
║  ┌───────────────────────────┐       ║
║  │ [🔵] Professional Blue    │       ║
║  │      #3B82F6      [Active]│       ║
║  └───────────────────────────┘       ║
║                                      ║
║  ┌───────────────────────────┐       ║
║  │ [🟢] Success Green        │       ║
║  │      #10B981              │       ║
║  └───────────────────────────┘       ║
║                                      ║
║  ... (6 more colors)                 ║
║                                      ║
╚══════════════════════════════════════╝
```

**Color Button Layout:**
- 48x48px color square on left
- Color name and hex code on right
- "Active" badge when selected
- Icon or checkmark inside color square

### 4️⃣ FOOTER (Dark Gradient)
```
╔══════════════════════════════════════╗
║  CURRENT SELECTION            [●]    ║
║  ─────────────────────────────────   ║
║  🤖 Auto CV                          ║
║  Professional Blue                   ║
╚══════════════════════════════════════╝
```
- Shows currently selected template + color
- Small color indicator dot
- Always visible at bottom

## Color Palette

### 8 Theme Colors:
1. 🔵 **Professional Blue** - #3B82F6 (Default)
2. 🟢 **Success Green** - #10B981
3. 🟣 **Creative Purple** - #8B5CF6
4. 🔴 **Bold Red** - #EF4444
5. 🟠 **Vibrant Orange** - #F59E0B
6. 🔷 **Modern Teal** - #14B8A6
7. 🌸 **Elegant Pink** - #EC4899
8. 🟦 **Classic Indigo** - #6366F1

## Animations

### Template Cards
```
Entry: opacity: 0 → 1, x: -20 → 0
Delay: 50ms per card (staggered)
Hover: scale: 1.0 → 1.02
```

### Color Buttons
```
Entry: opacity: 0 → 1, scale: 0.8 → 1.0
Delay: 50ms per button (staggered)
Hover: scale: 1.0 → 1.02
```

### Section Expand/Collapse
```
Duration: 300ms
Properties: height, opacity
Chevron: rotate(0deg) → rotate(180deg)
```

## Interaction States

### Template Cards:
- ⚪ **Default**: Gray border, white background
- 🎯 **Hover**: Border darkens, shadow appears, scales up
- ✅ **Selected**: Colored gradient, checkmark icon, shadow

### Color Buttons:
- ⚪ **Default**: Gray border, white background
- 🎯 **Hover**: Border darkens, scales up
- ✅ **Selected**: Dark border, shadow, checkmark overlay, "Active" badge

### Sections:
- 📖 **Expanded**: Content visible, chevron rotated down
- 📕 **Collapsed**: Content hidden, chevron rotated up

## Responsive Behavior

- **Scrolling**: Each section scrolls independently
- **Fixed Elements**: Header and footer remain visible
- **Max Height**: Template section limited to 384px (24rem)
- **Overflow**: Auto scroll when content exceeds max height

## Visual Hierarchy

1. **Level 1** - Header (Gradient, Large)
2. **Level 2** - Section Headers (Gradient buttons)
3. **Level 3** - Template/Color Cards
4. **Level 4** - Badges and labels
5. **Level 5** - Footer (Always visible)

## Accessibility Features

✅ Large touch targets (min 48x48px)
✅ Clear visual feedback on interaction
✅ High contrast text
✅ Descriptive labels
✅ Icons with text labels
✅ Smooth, purposeful animations
✅ Keyboard-accessible buttons

## Mobile Considerations

📱 Panel remains 320px wide (scales on smaller screens)
📱 Scrollable sections prevent overflow
📱 Large, touch-friendly buttons
📱 Clear visual hierarchy
📱 Single-column layout within sections
