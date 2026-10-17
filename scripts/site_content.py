"""Content for the Hali reference site: components, patterns and writing guidelines.

Every demo is real Hali markup. The site renders it live and shows the same markup as code, so the
documentation can never drift from what the components actually need.
"""


def I(name, cls=""):
    """Markup for an icon from the sprite."""
    extra = (" " + cls) if cls else ""
    return '<svg class="h-icon%s" aria-hidden="true"><use href="#i-%s"/></svg>' % (extra, name)


def MARK(cls="h-icon--lg h-icon--brand"):
    return '<svg class="h-icon %s" aria-hidden="true"><use href="#hali-mark"/></svg>' % cls


# ---------------------------------------------------------------------------------------------
# Components
# Each: id, title, group, blurb, demos [(label, html, options)], use [..], avoid [..], a11y [..]
# options: bg ("raised", "sunken", ...), layout ("cluster", "stack", "plain"), width (css max width)
# ---------------------------------------------------------------------------------------------

COMPONENTS = []


def add(**kw):
    kw.setdefault("use", [])
    kw.setdefault("avoid", [])
    kw.setdefault("a11y", [])
    COMPONENTS.append(kw)


add(
    id="button", title="Button", group="Actions",
    blurb="Buttons start actions. One bold button per view marks the main action. Everything else steps down.",
    demos=[
        ("Variants", """
<div class="h-cluster">
  <button class="h-button h-button--bold">Bold</button>
  <button class="h-button h-button--tonal">Tonal</button>
  <button class="h-button">Default</button>
  <button class="h-button h-button--outline">Outline</button>
  <button class="h-button h-button--subtle">Subtle</button>
  <button class="h-button h-button--danger">Delete</button>
  <button class="h-button h-button--danger-tonal">Remove</button>
  <button class="h-button h-button--link">Link button</button>
</div>""", {}),
        ("Sizes", """
<div class="h-cluster">
  <button class="h-button h-button--bold h-button--sm">Small, 28px</button>
  <button class="h-button h-button--bold">Medium, 36px</button>
  <button class="h-button h-button--bold h-button--lg">Large, 44px</button>
</div>""", {}),
        ("With icons", """
<div class="h-cluster">
  <button class="h-button h-button--bold">%s Create project</button>
  <button class="h-button h-button--outline">Export %s</button>
  <button class="h-button h-button--subtle h-button--icon" aria-label="Edit">%s</button>
  <button class="h-button h-button--tonal h-button--icon" aria-label="Add member">%s</button>
</div>""" % (I("plus"), I("download"), I("edit"), I("plus")), {}),
        ("States", """
<div class="h-cluster">
  <button class="h-button h-button--bold" disabled>Disabled</button>
  <button class="h-button" disabled>Disabled</button>
  <button class="h-button h-button--bold" aria-busy="true">Saving</button>
  <button class="h-button h-button--outline" aria-busy="true">Saving</button>
</div>""", {}),
        ("Group and full width", """
<div class="h-stack">
  <div class="h-button-group" role="group" aria-label="View">
    <button class="h-button h-button--outline">Day</button>
    <button class="h-button h-button--outline">Week</button>
    <button class="h-button h-button--outline">Month</button>
  </div>
  <button class="h-button h-button--bold h-button--block">Continue</button>
</div>""", {"width": "420px"}),
    ],
    use=["One bold button per view for the primary action.",
         "Start labels with a verb: Create project, Invite people, Save changes.",
         "Use tonal for a strong secondary action, default or outline for the rest, subtle for toolbars."],
    avoid=["Two bold buttons side by side. Pick the one that matters.",
           "Disabling a button without saying why nearby.",
           "Vague labels such as OK, Submit or Click here."],
    a11y=["Use a real `button` for actions and an `a` for navigation. Never a `div`.",
          "Icon only buttons need `aria-label`.",
          "Mark loading with `aria-busy=\"true\"`. The label stays in the DOM for assistive technology.",
          "Prefer `aria-disabled=\"true\"` over `disabled` when the button should stay focusable to explain itself."],
)

add(
    id="link", title="Link", group="Actions",
    blurb="Links navigate. Inside text they are always underlined, because color alone is not enough.",
    demos=[
        ("In text", """
<p class="h-body-lg" style="max-width:56ch">Read the <a href="#link">accessibility guide</a> before shipping a new component, or see how
<a href="#link">versioning</a> works. External links get an icon:
<a href="#link">Nord palette %s</a>.</p>""" % I("external", "h-icon--sm"), {}),
        ("Subtle and standalone", """
<div class="h-cluster h-gap-16">
  <a class="h-button h-button--link" href="#link">View all projects %s</a>
  <a class="h-text-subtle" href="#link">Secondary link</a>
</div>""" % I("arrow-right", "h-icon--sm"), {}),
    ],
    use=["Describe where the link goes: 'Read the accessibility guide', not 'Click here'."],
    avoid=["Removing the underline inside running text.", "Opening links in a new tab without telling people."],
    a11y=["Links are announced by their text, so the text must make sense out of context.",
          "Add a visually hidden hint when a link opens a new tab."],
)

add(
    id="fields", title="Text field", group="Forms",
    blurb="Fields collect text. Every field has a visible label, optional help text, and an error that says how to fix it.",
    demos=[
        ("Field with help", """
<div class="h-field">
  <label class="h-label" for="fld-name">Project name</label>
  <input class="h-input" id="fld-name" type="text" placeholder="Aurora" aria-describedby="fld-name-help">
  <div class="h-help" id="fld-name-help">Visible to everyone in your workspace.</div>
</div>""", {"width": "360px"}),
        ("Required and invalid", """
<div class="h-field">
  <label class="h-label" for="fld-email" data-required>Work email</label>
  <input class="h-input" id="fld-email" type="email" value="alex@acme" aria-invalid="true" aria-describedby="fld-email-err">
  <div class="h-error" id="fld-email-err">%s<span>Enter a full address, like alex@acme.com.</span></div>
</div>""" % I("error", "h-icon--sm"), {"width": "360px"}),
        ("Disabled and sizes", """
<div class="h-stack" style="max-width:360px">
  <input class="h-input h-input--sm" placeholder="Small, 28px" aria-label="Small">
  <input class="h-input" placeholder="Medium, 36px" aria-label="Medium">
  <input class="h-input h-input--lg" placeholder="Large, 44px" aria-label="Large">
  <input class="h-input" value="Locked by an admin" disabled aria-label="Disabled">
</div>""", {}),
        ("Search with icon", """
<div class="h-input-group" style="max-width:360px">
  %s
  <input class="h-input" type="search" placeholder="Search projects" aria-label="Search projects">
</div>""" % I("search"), {}),
        ("Textarea and select", """
<div class="h-stack" style="max-width:360px">
  <div class="h-field">
    <label class="h-label" for="fld-desc">Description</label>
    <textarea class="h-textarea" id="fld-desc" placeholder="What is this project about?"></textarea>
  </div>
  <div class="h-field">
    <label class="h-label" for="fld-role">Role</label>
    <div class="h-select">
      <select id="fld-role">
        <option>Viewer</option>
        <option>Editor</option>
        <option>Admin</option>
      </select>
      %s
    </div>
  </div>
</div>""" % I("chevron-down"), {}),
    ],
    use=["Put the label above the field, left aligned.",
         "Say what the field is for in help text, and say how to recover in error text.",
         "Mark required fields with `data-required`, and say so once at the top of long forms."],
    avoid=["Using a placeholder as the label. It disappears while typing.",
           "Error text that blames: 'Invalid input'. Say what to do instead."],
    a11y=["Link help and error text with `aria-describedby`.",
          "Set `aria-invalid=\"true\"` on invalid fields and move focus to the first one on submit.",
          "The field border is 3:1 against every surface, as required for UI components."],
)

add(
    id="choice", title="Checkbox and radio", group="Forms",
    blurb="Checkboxes select any number of options. Radios select exactly one.",
    demos=[
        ("Checkbox", """
<fieldset class="h-fieldset">
  <legend>Notify me about</legend>
  <label class="h-check"><input type="checkbox" checked><span>Mentions</span></label>
  <label class="h-check"><input type="checkbox"><span>Comments on my work</span></label>
  <label class="h-check"><input type="checkbox" id="chk-ind"><span>Everything (some selected)</span></label>
  <label class="h-check"><input type="checkbox" disabled><span>Weekly digest (unavailable)</span></label>
</fieldset>
<script>document.getElementById('chk-ind').indeterminate = true;</script>""", {}),
        ("Radio group", """
<fieldset class="h-fieldset">
  <legend>Visibility</legend>
  <label class="h-check"><input type="radio" name="vis" checked><span>Private to me</span></label>
  <label class="h-check"><input type="radio" name="vis"><span>Everyone in the workspace</span></label>
  <label class="h-check"><input type="radio" name="vis" disabled><span>Public (requires an upgrade)</span></label>
</fieldset>""", {}),
    ],
    use=["Write labels so they make sense when read alone.", "Use a fieldset and legend to group related options."],
    avoid=["Radios for a single yes or no. Use a checkbox or a switch."],
    a11y=["Wrap the input and text in one `label`, so the whole row is clickable.",
          "Indeterminate is set from script: `input.indeterminate = true`."],
)

add(
    id="switch", title="Switch", group="Forms",
    blurb="Switches turn a setting on or off immediately. No save button is needed.",
    demos=[
        ("States", """
<div class="h-stack h-gap-12">
  <label class="h-switch"><input type="checkbox" role="switch" checked><span>Email notifications</span></label>
  <label class="h-switch"><input type="checkbox" role="switch"><span>Push notifications</span></label>
  <label class="h-switch"><input type="checkbox" role="switch" disabled><span>SMS (unavailable)</span></label>
</div>""", {}),
    ],
    use=["Use for settings that take effect immediately."],
    avoid=["Switches in forms that need a Save button. Use a checkbox there."],
    a11y=["Keep `role=\"switch\"` on the checkbox so the state is announced as on or off.",
          "On and off are told apart by thumb position and size, not color alone."],
)

add(
    id="segmented", title="Segmented control", group="Forms",
    blurb="A segmented control switches between two to five views or modes of the same content.",
    demos=[
        ("Single select", """
<div class="h-segmented" role="group" aria-label="Layout" data-segmented>
  <button type="button" aria-pressed="true">%s List</button>
  <button type="button" aria-pressed="false">%s Grid</button>
  <button type="button" aria-pressed="false">%s Chart</button>
</div>""" % (I("menu", "h-icon--sm"), I("grid", "h-icon--sm"), I("chart", "h-icon--sm")), {}),
    ],
    use=["Use when the options are peers and few."],
    avoid=["More than five segments. Use tabs or a select."],
    a11y=["Each segment is a button with `aria-pressed`. Group them with `role=\"group\"` and a label."],
)

add(
    id="chip", title="Chip", group="Forms",
    blurb="Chips filter, tag or toggle. They are compact and rounded to 8px, like Material.",
    demos=[
        ("Filter chips", """
<div class="h-cluster" role="group" aria-label="Filter by status" data-chips>
  <button class="h-chip" aria-pressed="true">%s Open</button>
  <button class="h-chip" aria-pressed="false">In review</button>
  <button class="h-chip" aria-pressed="false">Blocked</button>
  <button class="h-chip" aria-pressed="false">Done</button>
</div>""" % I("check"), {}),
        ("Input chips", """
<div class="h-cluster">
  <span class="h-chip">Design<button class="h-chip__remove" aria-label="Remove Design">%s</button></span>
  <span class="h-chip">Accessibility<button class="h-chip__remove" aria-label="Remove Accessibility">%s</button></span>
</div>""" % (I("close", "h-icon--sm"), I("close", "h-icon--sm")), {}),
    ],
    a11y=["Toggle chips use `aria-pressed`. Removable chips need an `aria-label` that names what is removed."],
)

add(
    id="lozenge", title="Lozenge, badge and dot", group="Display",
    blurb="Small status markers. Lozenges label state, badges count, dots hint.",
    demos=[
        ("Subtle lozenges", """
<div class="h-cluster">
  <span class="h-lozenge">Draft</span>
  <span class="h-lozenge h-is-brand">In progress</span>
  <span class="h-lozenge h-is-success">%s Done</span>
  <span class="h-lozenge h-is-warning">%s At risk</span>
  <span class="h-lozenge h-is-danger">%s Blocked</span>
  <span class="h-lozenge h-is-info">Review</span>
  <span class="h-lozenge h-is-discovery">New</span>
</div>""" % (I("check"), I("warning"), I("error")), {}),
        ("Bold lozenges", """
<div class="h-cluster">
  <span class="h-lozenge h-lozenge--bold h-is-neutral">Draft</span>
  <span class="h-lozenge h-lozenge--bold h-is-brand">In progress</span>
  <span class="h-lozenge h-lozenge--bold h-is-success">Done</span>
  <span class="h-lozenge h-lozenge--bold h-is-warning">At risk</span>
  <span class="h-lozenge h-lozenge--bold h-is-danger">Blocked</span>
  <span class="h-lozenge h-lozenge--bold h-is-info">Review</span>
  <span class="h-lozenge h-lozenge--bold h-is-discovery">New</span>
</div>""", {}),
        ("Badges and dots", """
<div class="h-cluster h-gap-16">
  <span class="h-badge">3</span>
  <span class="h-badge h-is-danger">12</span>
  <span class="h-badge h-is-success">99+</span>
  <span class="h-cluster h-gap-4"><span class="h-dot h-is-success"></span> Online</span>
  <span class="h-cluster h-gap-4"><span class="h-dot h-is-warning"></span> Away</span>
  <span class="h-cluster h-gap-4"><span class="h-dot h-is-danger"></span> Offline</span>
</div>""", {}),
    ],
    use=["Add the status class (`h-is-success` and so on) to pick the color family.",
         "Pair color with an icon or a word so state never depends on color alone."],
    avoid=["Using bold lozenges for every row of a table. Reserve bold for the one that needs attention."],
    a11y=["A dot has no text. Give it a nearby text label or `aria-label`, never a lone colored circle."],
)

add(
    id="avatar", title="Avatar", group="Display",
    blurb="Avatars identify people. Initials sit on a tonal accent color.",
    demos=[
        ("Sizes and colors", """
<div class="h-cluster h-gap-12">
  <span class="h-avatar h-avatar--sm h-accent-teal" aria-label="Ana Ruiz">AR</span>
  <span class="h-avatar h-accent-cyan" aria-label="Ben Cole">BC</span>
  <span class="h-avatar h-avatar--lg h-accent-purple" aria-label="Cam Diaz">CD</span>
  <span class="h-avatar h-avatar--xl h-accent-orange" aria-label="Dee Evans">DE</span>
  <span class="h-avatar h-accent-green" aria-label="Eli Fox">EF</span>
  <span class="h-avatar h-accent-yellow" aria-label="Fay Gray">FG</span>
</div>""", {}),
        ("Group", """
<div class="h-avatar-group" role="group" aria-label="Team members">
  <span class="h-avatar h-accent-teal" aria-label="Ana Ruiz">AR</span>
  <span class="h-avatar h-accent-purple" aria-label="Ben Cole">BC</span>
  <span class="h-avatar h-accent-orange" aria-label="Cam Diaz">CD</span>
  <span class="h-avatar h-accent-blue" aria-label="3 more">+3</span>
</div>""", {}),
    ],
    a11y=["Initials are read as letters. Add `aria-label` with the full name."],
)

add(
    id="card", title="Card", group="Display",
    blurb="Cards group related content on a raised surface. Depth is tone first, shadow only when you ask for it.",
    demos=[
        ("Basic, elevated and outlined", """
<div class="h-grid" style="--h-col:200px">
  <article class="h-card">
    <h3 class="h-card__title">Basic</h3>
    <p class="h-card__meta">Raised surface and a quiet border</p>
  </article>
  <article class="h-card h-card--elevated">
    <h3 class="h-card__title">Elevated</h3>
    <p class="h-card__meta">Adds a soft shadow</p>
  </article>
  <article class="h-card h-card--outlined">
    <h3 class="h-card__title">Outlined</h3>
    <p class="h-card__meta">No fill, border only</p>
  </article>
</div>""", {}),
        ("With header and actions", """
<article class="h-card" style="max-width:420px">
  <header class="h-card__header">
    <div>
      <h3 class="h-card__title">Aurora redesign</h3>
      <p class="h-card__meta">Updated 2 hours ago</p>
    </div>
    <span class="h-lozenge h-is-brand">In progress</span>
  </header>
  <p class="h-card__body">Refresh the onboarding flow and ship the new dashboard to all workspaces.</p>
  <footer class="h-card__footer">
    <button class="h-button h-button--subtle">Archive</button>
    <button class="h-button h-button--tonal">Open project</button>
  </footer>
</article>""", {}),
        ("Interactive", """
<a class="h-card h-card--interactive" href="#card" style="max-width:320px">
  <h3 class="h-card__title">Whole card is a link</h3>
  <p class="h-card__meta">Hover and focus show a state layer</p>
</a>""", {}),
    ],
    use=["Keep one idea per card.", "Make a whole card clickable only when it has a single destination."],
    avoid=["Nesting cards inside cards. Use a divider or a sunken surface instead."],
    a11y=["An interactive card is an `a` or `button`. Do not nest other links or buttons inside it."],
)

add(
    id="alert", title="Alert", group="Feedback",
    blurb="Alerts sit inside the page and tell people something that needs their attention. They never disappear on their own.",
    demos=[
        ("Statuses", """
<div class="h-stack h-gap-12">
  <div class="h-alert h-is-info" role="status">%s<div><div class="h-alert__title">Scheduled maintenance</div><div class="h-alert__body">Hali Cloud will be read only on Saturday from 02:00 to 03:00 UTC.</div></div></div>
  <div class="h-alert h-is-success" role="status">%s<div><div class="h-alert__title">Changes saved</div><div class="h-alert__body">Everyone in the workspace can see your update.</div></div></div>
  <div class="h-alert h-is-warning" role="status">%s<div><div class="h-alert__title">Storage is almost full</div><div class="h-alert__body">You have used 92%% of your plan.</div></div></div>
  <div class="h-alert h-is-danger" role="alert">%s<div><div class="h-alert__title">Payment failed</div><div class="h-alert__body">Your card was declined. Update it to keep your plan active.</div></div></div>
  <div class="h-alert h-is-discovery" role="status">%s<div><div class="h-alert__title">Try keyboard shortcuts</div><div class="h-alert__body">Press <kbd class="h-kbd">?</kbd> anywhere to see them all.</div></div></div>
</div>""" % (I("info"), I("success"), I("warning"), I("error"), I("star")), {"width": "640px"}),
        ("With actions and dismiss", """
<div class="h-alert h-is-warning" role="status" style="max-width:640px">
  %s
  <div>
    <div class="h-alert__title">3 members have not accepted their invite</div>
    <div class="h-alert__body">Invites expire in 7 days.</div>
    <div class="h-alert__actions">
      <button class="h-button h-button--sm h-button--outline">Resend invites</button>
      <button class="h-button h-button--sm h-button--subtle">View members</button>
    </div>
  </div>
  <button class="h-button h-button--subtle h-button--icon h-button--sm" aria-label="Dismiss">%s</button>
</div>""" % (I("warning"), I("close")), {}),
    ],
    use=["Lead with what happened, then what to do.", "Use `role=\"alert\"` only for urgent problems. Use `role=\"status\"` for the rest."],
    avoid=["Stacking more than two alerts. Combine or prioritize."],
    a11y=["Status is carried by the icon and the title as well as the color.",
          "Dismiss buttons need `aria-label`."],
)

add(
    id="banner", title="Banner", group="Feedback",
    blurb="Banners span the full width of the page for system wide messages. Use sparingly.",
    demos=[
        ("Statuses", """
<div class="h-stack h-gap-8" style="border-radius:12px;overflow:hidden">
  <div class="h-banner h-is-brand" role="status">%s New: dark mode is now the default. <a href="#banner">Learn more</a></div>
  <div class="h-banner h-is-warning" role="status">%s Your trial ends in 3 days. <a href="#banner">Choose a plan</a></div>
  <div class="h-banner h-is-danger" role="alert">%s We are investigating a login issue. <a href="#banner">Status page</a></div>
</div>""" % (I("info"), I("warning"), I("error")), {}),
    ],
    use=["Place at the very top of the page, above the top bar."],
    avoid=["Using a banner for something only one user needs to see. Use an alert."],
    a11y=["Bold banners keep 4.5:1 between text and fill in both themes."],
)

add(
    id="toast", title="Toast", group="Feedback",
    blurb="Toasts confirm a result without interrupting. They are brief, appear at the bottom left, and can be dismissed.",
    demos=[
        ("Static examples", """
<div class="h-stack h-gap-12" style="align-items:flex-start">
  <div class="h-toast h-is-success" role="status" style="animation:none">%s<span class="h-toast__message">Project archived</span><button class="h-button h-button--link">Undo</button></div>
  <div class="h-toast h-is-danger" role="alert" style="animation:none">%s<span class="h-toast__message">Could not send invite</span><button class="h-button h-button--link">Retry</button></div>
</div>""" % (I("success"), I("error")), {}),
        ("Try it", """
<div class="h-cluster">
  <button class="h-button h-button--outline" data-toast="success|Changes saved">Show success</button>
  <button class="h-button h-button--outline" data-toast="info|Your export is ready">Show info</button>
  <button class="h-button h-button--outline" data-toast="danger|Something went wrong">Show error</button>
</div>""", {}),
    ],
    use=["Keep the message under 10 words and put the action on the right.", "Always offer Undo for destructive actions instead of a confirm dialog when it is possible."],
    avoid=["Putting the only way to complete a task inside a toast."],
    a11y=["Use `role=\"status\"` for information and `role=\"alert\"` for errors.",
          "Leave toasts on screen for at least 5 seconds, and pause the timer on hover and focus."],
)

add(
    id="tabs", title="Tabs", group="Navigation",
    blurb="Tabs switch between related panels on one page without leaving it.",
    demos=[
        ("Tabs", """
<div data-tabs style="max-width:560px">
  <div class="h-tabs" role="tablist" aria-label="Project sections">
    <button class="h-tab" role="tab" id="tab-1" aria-selected="true" aria-controls="panel-1">Overview</button>
    <button class="h-tab" role="tab" id="tab-2" aria-selected="false" aria-controls="panel-2" tabindex="-1">Activity %s</button>
    <button class="h-tab" role="tab" id="tab-3" aria-selected="false" aria-controls="panel-3" tabindex="-1">Settings</button>
  </div>
  <div class="h-tabpanel" role="tabpanel" id="panel-1" aria-labelledby="tab-1">The overview shows progress, owners and the next milestone.</div>
  <div class="h-tabpanel" role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>Activity lists every change, newest first.</div>
  <div class="h-tabpanel" role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>Settings control visibility, members and integrations.</div>
</div>""" % '<span class="h-badge">4</span>', {}),
    ],
    use=["Keep tab labels to one or two words.", "Use tabs for peers. Use a stepper or page for sequences."],
    avoid=["More than seven tabs. Group or use a select."],
    a11y=["Arrow keys move between tabs, Home and End jump to the ends. The selected tab is the only one in the tab order (`tabindex=\"-1\"` on the rest)."],
)

add(
    id="breadcrumbs", title="Breadcrumbs", group="Navigation",
    blurb="Breadcrumbs show where the page sits in the hierarchy.",
    demos=[
        ("Breadcrumbs", """
<nav aria-label="Breadcrumb">
  <ol class="h-breadcrumbs">
    <li><a href="#breadcrumbs">Workspace</a></li>
    <li><a href="#breadcrumbs">Projects</a></li>
    <li><a href="#breadcrumbs">Aurora redesign</a></li>
    <li><span aria-current="page">Settings</span></li>
  </ol>
</nav>""", {}),
    ],
    a11y=["Wrap in `nav` with `aria-label=\"Breadcrumb\"`. Mark the current page with `aria-current=\"page\"`."],
)

add(
    id="pagination", title="Pagination", group="Navigation",
    blurb="Pagination moves through long result sets.",
    demos=[
        ("Pagination", """
<nav aria-label="Pagination">
  <ul class="h-pagination">
    <li><button class="h-button h-button--subtle h-button--icon h-button--sm" aria-label="Previous page" disabled>%s</button></li>
    <li><button class="h-button h-button--subtle h-button--icon h-button--sm" aria-current="page" aria-label="Page 1, current page">1</button></li>
    <li><button class="h-button h-button--subtle h-button--icon h-button--sm" aria-label="Page 2">2</button></li>
    <li><button class="h-button h-button--subtle h-button--icon h-button--sm" aria-label="Page 3">3</button></li>
    <li><span class="h-text-subtle" aria-hidden="true">...</span></li>
    <li><button class="h-button h-button--subtle h-button--icon h-button--sm" aria-label="Page 12">12</button></li>
    <li><button class="h-button h-button--subtle h-button--icon h-button--sm" aria-label="Next page">%s</button></li>
  </ul>
</nav>""" % (I("chevron-left"), I("chevron-right")), {}),
    ],
    a11y=["Label every page button with its number and mark the current one with `aria-current=\"page\"`."],
)

add(
    id="topbar", title="Top bar", group="Navigation",
    blurb="The top bar holds the brand, primary navigation and global actions. It is 56px tall and sticks to the top.",
    demos=[
        ("Top bar", """
<header class="h-topbar h-topbar--static" style="border:1px solid var(--hali-border-default);border-radius:12px">
  <a class="h-topbar__brand" href="#topbar">%s Hali</a>
  <nav class="h-topbar__nav" aria-label="Primary">
    <a class="h-topbar__link" href="#topbar" aria-current="page">Projects</a>
    <a class="h-topbar__link" href="#topbar">Reports</a>
    <a class="h-topbar__link" href="#topbar">People</a>
  </nav>
  <div class="h-topbar__actions">
    <button class="h-button h-button--subtle h-button--icon" aria-label="Search">%s</button>
    <button class="h-button h-button--subtle h-button--icon" aria-label="Notifications, 3 unread">%s</button>
    <span class="h-avatar h-accent-teal" role="img" aria-label="Your account">AR</span>
  </div>
</header>""" % (MARK("h-icon--lg h-icon--brand"), I("search"), I("bell")), {"layout": "plain"}),
    ],
    a11y=["Wrap links in `nav` with a label. Mark the current section with `aria-current=\"page\"`.",
          "Provide a skip link (`h-skip`) as the first focusable element on the page."],
)

add(
    id="sidenav", title="Side navigation", group="Navigation",
    blurb="Side navigation lists the sections of an app. It is 264px wide, or an 80px rail when space is tight.",
    demos=[
        ("Side navigation", """
<nav class="h-sidenav" aria-label="Project" style="width:264px;border:1px solid var(--hali-border-default);border-radius:12px">
  <a class="h-sidenav__item" href="#sidenav" aria-current="page">%s Overview</a>
  <a class="h-sidenav__item" href="#sidenav">%s Board</a>
  <a class="h-sidenav__item" href="#sidenav">%s Inbox <span class="h-badge h-is-danger">4</span></a>
  <a class="h-sidenav__item" href="#sidenav">%s Reports</a>
  <div class="h-sidenav__section">Manage</div>
  <a class="h-sidenav__item" href="#sidenav">%s Members</a>
  <a class="h-sidenav__item" href="#sidenav">%s Settings <span class="h-lozenge h-is-discovery">New</span></a>
</nav>""" % (I("home"), I("grid"), I("inbox"), I("chart"), I("user"), I("sliders")), {"layout": "plain"}),
        ("Rail", """
<nav class="h-sidenav h-sidenav--rail" aria-label="Project rail" style="border:1px solid var(--hali-border-default);border-radius:12px">
  <a class="h-sidenav__item" href="#sidenav" aria-current="page">%s Home</a>
  <a class="h-sidenav__item" href="#sidenav">%s Board</a>
  <a class="h-sidenav__item" href="#sidenav">%s Inbox</a>
  <a class="h-sidenav__item" href="#sidenav">%s Reports</a>
</nav>""" % (I("home"), I("grid"), I("inbox"), I("chart")), {"layout": "plain"}),
    ],
    a11y=["The current item uses `aria-current=\"page\"` and a tonal fill, so it is not color only."],
)

add(
    id="menu", title="Menu and dropdown", group="Overlays",
    blurb="Menus list actions for one item. Open them from a button and close them on Escape or when focus leaves.",
    demos=[
        ("Menu", """
<div class="h-menu" role="menu" aria-label="Project actions" style="max-width:260px">
  <button class="h-menu__item" role="menuitem">%s Rename <span class="h-menu__shortcut">R</span></button>
  <button class="h-menu__item" role="menuitem">%s Duplicate <span class="h-menu__shortcut">D</span></button>
  <button class="h-menu__item" role="menuitem">%s Copy link</button>
  <div class="h-menu__sep" role="separator"></div>
  <div class="h-menu__label">Danger zone</div>
  <button class="h-menu__item h-menu__item--danger" role="menuitem">%s Delete project</button>
  <button class="h-menu__item" role="menuitem" disabled>Archive (unavailable)</button>
</div>""" % (I("edit"), I("copy"), I("link"), I("trash")), {}),
        ("Dropdown", """
<div class="h-dropdown" data-dropdown>
  <button class="h-button h-button--outline" aria-haspopup="menu" aria-expanded="false" data-dropdown-toggle>Actions %s</button>
  <div class="h-menu" role="menu" aria-label="Actions" hidden>
    <button class="h-menu__item" role="menuitem">%s Export CSV</button>
    <button class="h-menu__item" role="menuitem">%s Share</button>
    <div class="h-menu__sep" role="separator"></div>
    <button class="h-menu__item h-menu__item--danger" role="menuitem">%s Delete</button>
  </div>
</div>""" % (I("chevron-down", "h-icon--sm"), I("download"), I("link"), I("trash")), {"minheight": "220px"}),
    ],
    a11y=["The trigger has `aria-haspopup=\"menu\"` and `aria-expanded`.",
          "Arrow keys move through items, Escape closes and returns focus to the trigger. The optional `js/hali.js` does this for markup that uses `data-dropdown`."],
)

add(
    id="tooltip", title="Tooltip", group="Overlays",
    blurb="Tooltips name or briefly explain a control. They show on hover and on keyboard focus.",
    demos=[
        ("Tooltip", """
<div class="h-cluster h-gap-16">
  <button class="h-button h-button--outline h-button--icon" aria-label="Copy link" data-tooltip="Copy link">%s</button>
  <button class="h-button h-button--outline h-button--icon" aria-label="Delete" data-tooltip="Delete" data-tooltip-position="bottom">%s</button>
</div>""" % (I("link"), I("trash")), {"minheight": "120px"}),
    ],
    use=["Name the action in two or three words."],
    avoid=["Putting essential information in a tooltip. Touch users and screen magnifier users can miss it."],
    a11y=["Do not rely on the tooltip as the only name. Icon only buttons keep their `aria-label`."],
)

add(
    id="dialog", title="Dialog", group="Overlays",
    blurb="Dialogs interrupt for a decision. Built on the native dialog element, so focus trapping, Escape and the backdrop come free.",
    demos=[
        ("Confirmation", """
<button class="h-button h-button--danger-tonal" data-dialog-open="dlg-delete">%s Delete project</button>

<dialog class="h-dialog h-dialog--sm" id="dlg-delete" aria-labelledby="dlg-delete-title">
  <div class="h-dialog__header">
    <h2 class="h-dialog__title" id="dlg-delete-title">Delete Aurora redesign?</h2>
    <button class="h-button h-button--subtle h-button--icon h-button--sm" aria-label="Close" data-dialog-close>%s</button>
  </div>
  <div class="h-dialog__body">
    <p>This removes the project and its 48 tasks for everyone. You can restore it from the trash for 30 days.</p>
  </div>
  <div class="h-dialog__footer">
    <button class="h-button h-button--subtle" data-dialog-close>Cancel</button>
    <button class="h-button h-button--danger" data-dialog-close>Delete project</button>
  </div>
</dialog>""" % (I("trash"), I("close")), {}),
        ("Form dialog", """
<button class="h-button h-button--bold" data-dialog-open="dlg-invite">%s Invite people</button>

<dialog class="h-dialog" id="dlg-invite" aria-labelledby="dlg-invite-title">
  <div class="h-dialog__header">
    <h2 class="h-dialog__title" id="dlg-invite-title">Invite people</h2>
    <button class="h-button h-button--subtle h-button--icon h-button--sm" aria-label="Close" data-dialog-close>%s</button>
  </div>
  <div class="h-dialog__body h-stack">
    <div class="h-field">
      <label class="h-label" for="dlg-email">Email addresses</label>
      <input class="h-input" id="dlg-email" type="text" placeholder="name@company.com, name@company.com">
      <div class="h-help">Separate addresses with commas.</div>
    </div>
    <div class="h-field">
      <label class="h-label" for="dlg-role">Role</label>
      <div class="h-select"><select id="dlg-role"><option>Viewer</option><option>Editor</option></select>%s</div>
    </div>
  </div>
  <div class="h-dialog__footer">
    <button class="h-button h-button--subtle" data-dialog-close>Cancel</button>
    <button class="h-button h-button--bold" data-dialog-close>Send invites</button>
  </div>
</dialog>""" % (I("plus"), I("close"), I("chevron-down")), {}),
    ],
    use=["Title states the question or the task. The confirm button repeats the verb: 'Delete project', not 'OK'.",
         "Cancel is always on the left of the confirm action, as a subtle button."],
    avoid=["Dialogs for information that can live in the page.", "Stacking dialogs."],
    a11y=["Open with `showModal()`. Focus moves inside and returns to the opener on close.",
          "Label with `aria-labelledby` pointing at the title.",
          "Never put the only copy of important information in a dialog."],
)

add(
    id="sheet", title="Side sheet", group="Overlays",
    blurb="A side sheet shows detail next to the page without leaving it. 420px wide on desktop.",
    demos=[
        ("Side sheet", """
<div class="doc-stage" style="height:340px">
  <aside class="h-sheet" aria-labelledby="sheet-title">
    <div class="h-dialog__header">
      <h2 class="h-dialog__title" id="sheet-title">Task details</h2>
      <button class="h-button h-button--subtle h-button--icon h-button--sm" aria-label="Close">%s</button>
    </div>
    <div class="h-dialog__body h-stack h-gap-12">
      <div class="h-cluster"><span class="h-lozenge h-is-brand">In progress</span><span class="h-lozenge">Design</span></div>
      <p>Update the empty states in the dashboard to follow the new content guidelines.</p>
      <dl class="h-stack h-gap-8">
        <div class="h-split"><dt class="h-text-subtle">Assignee</dt><dd><span class="h-cluster h-gap-8"><span class="h-avatar h-avatar--sm h-accent-teal">AR</span>Ana Ruiz</span></dd></div>
        <div class="h-split"><dt class="h-text-subtle">Due</dt><dd>Oct 24, 2026</dd></div>
      </dl>
    </div>
    <div class="h-dialog__footer" style="margin-top:auto"><button class="h-button h-button--subtle">Close</button><button class="h-button h-button--bold">Save</button></div>
  </aside>
</div>""" % I("close"), {"layout": "plain"}),
    ],
    a11y=["A modal sheet behaves like a dialog. A non modal sheet is a `complementary` landmark and does not trap focus."],
)

add(
    id="table", title="Table", group="Data",
    blurb="Tables compare records across attributes. Numbers align right and use tabular figures.",
    demos=[
        ("Table with toolbar", """
<div class="h-table-wrap">
  <div class="h-toolbar">
    <div class="h-input-group" style="width:240px">%s<input class="h-input h-input--sm" type="search" placeholder="Filter projects" aria-label="Filter projects"></div>
    <button class="h-button h-button--outline h-button--sm">%s Filter</button>
    <span class="h-spacer"></span>
    <button class="h-button h-button--bold h-button--sm">%s New project</button>
  </div>
  <table class="h-table" data-sortable>
    <caption class="h-sr-only">Projects</caption>
    <thead>
      <tr>
        <th scope="col" aria-sort="ascending"><button class="h-table__sort">Project %s</button></th>
        <th scope="col">Status</th>
        <th scope="col">Owner</th>
        <th scope="col" data-numeric><button class="h-table__sort">Budget %s</button></th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Aurora redesign</td><td><span class="h-lozenge h-is-brand">In progress</span></td><td><span class="h-cluster h-gap-8"><span class="h-avatar h-avatar--sm h-accent-teal">AR</span>Ana Ruiz</span></td><td data-numeric>$48,000</td></tr>
      <tr aria-selected="true"><td>Billing migration</td><td><span class="h-lozenge h-is-warning">%s At risk</span></td><td><span class="h-cluster h-gap-8"><span class="h-avatar h-avatar--sm h-accent-purple">BC</span>Ben Cole</span></td><td data-numeric>$120,500</td></tr>
      <tr><td>Mobile app</td><td><span class="h-lozenge h-is-success">%s Done</span></td><td><span class="h-cluster h-gap-8"><span class="h-avatar h-avatar--sm h-accent-orange">CD</span>Cam Diaz</span></td><td data-numeric>$76,250</td></tr>
      <tr><td>Data warehouse</td><td><span class="h-lozenge h-is-danger">%s Blocked</span></td><td><span class="h-cluster h-gap-8"><span class="h-avatar h-avatar--sm h-accent-green">EF</span>Eli Fox</span></td><td data-numeric>$31,900</td></tr>
    </tbody>
  </table>
</div>""" % (I("search"), I("filter"), I("plus"), I("arrow-up-down", "h-icon--sm"), I("arrow-up-down", "h-icon--sm"), I("warning"), I("check"), I("error")), {"layout": "plain"}),
        ("Dense", """
<div class="h-table-wrap" style="max-width:520px">
  <table class="h-table h-table--dense">
    <caption class="h-sr-only">Recent deploys</caption>
    <thead><tr><th scope="col">Build</th><th scope="col">Branch</th><th scope="col" data-numeric>Time</th></tr></thead>
    <tbody>
      <tr><td><code class="h-code">#4182</code></td><td>main</td><td data-numeric>2m 14s</td></tr>
      <tr><td><code class="h-code">#4181</code></td><td>feat/tokens</td><td data-numeric>2m 40s</td></tr>
      <tr><td><code class="h-code">#4180</code></td><td>fix/focus</td><td data-numeric>1m 58s</td></tr>
    </tbody>
  </table>
</div>""", {}),
    ],
    use=["Left align text, right align numbers, and keep column headers short.",
         "Use the selected row state for bulk actions."],
    avoid=["Using a table for layout.", "Hiding important columns on small screens without a way to get them back."],
    a11y=["Use `th scope=\"col\"`, a `caption` or `aria-label`, and `aria-sort` on the sorted column.",
          "Sortable headers contain a real `button`. Wrap wide tables in `h-table-wrap` so they scroll without breaking the page."],
)

add(
    id="progress", title="Progress and spinner", group="Feedback",
    blurb="Progress shows how far along something is. Spinners show that something is happening and the time is unknown.",
    demos=[
        ("Progress", """
<div class="h-stack h-gap-16" style="max-width:420px">
  <div><div class="h-split h-body-sm"><span>Uploading</span><span class="h-tabular">64%</span></div>
    <div class="h-progress h-mt-8" role="progressbar" aria-label="Uploading" aria-valuenow="64" aria-valuemin="0" aria-valuemax="100"><div class="h-progress__bar" style="width:64%"></div></div></div>
  <div><div class="h-split h-body-sm"><span>Storage</span><span class="h-tabular">92%</span></div>
    <div class="h-progress h-is-warning h-mt-8" role="progressbar" aria-label="Storage used" aria-valuenow="92" aria-valuemin="0" aria-valuemax="100"><div class="h-progress__bar" style="width:92%"></div></div></div>
  <div><div class="h-body-sm">Preparing export</div>
    <div class="h-progress h-progress--indeterminate h-mt-8" role="progressbar" aria-label="Preparing export"><div class="h-progress__bar"></div></div></div>
</div>""", {}),
        ("Spinner", """
<div class="h-cluster h-gap-24">
  <span class="h-spinner" role="status" aria-label="Loading"></span>
  <span class="h-spinner h-spinner--lg" role="status" aria-label="Loading"></span>
</div>""", {}),
    ],
    use=["Prefer determinate progress whenever you know the total.", "Show a spinner only after 400ms. Faster than that, it flickers."],
    avoid=["A spinner with no label for longer than a few seconds. Say what is happening."],
    a11y=["Progress bars need a name and `aria-valuenow`. Indeterminate bars omit the value.",
          "Under reduced motion the indeterminate bar becomes a still, dimmed bar."],
)

add(
    id="skeleton", title="Skeleton", group="Feedback",
    blurb="Skeletons hold the shape of content while it loads, so the page does not jump.",
    demos=[
        ("Skeleton", """
<div aria-busy="true" style="max-width:420px">
  <span class="h-sr-only" role="status">Loading</span>
  <div class="h-card">
    <div class="h-cluster h-gap-12" style="flex-wrap:nowrap">
      <span class="h-skeleton h-skeleton--circle"></span>
      <div class="h-stack h-gap-8" style="flex:1"><span class="h-skeleton h-skeleton--text" style="width:50%"></span><span class="h-skeleton h-skeleton--text" style="width:30%"></span></div>
    </div>
    <div class="h-stack h-gap-8 h-mt-16"><span class="h-skeleton h-skeleton--text"></span><span class="h-skeleton h-skeleton--text"></span><span class="h-skeleton h-skeleton--text" style="width:70%"></span></div>
  </div>
</div>""", {}),
    ],
    a11y=["Set `aria-busy=\"true\"` on the loading region and include a visually hidden 'Loading' message.",
          "The shimmer stops under reduced motion."],
)

add(
    id="empty", title="Empty state", group="Feedback",
    blurb="Empty states explain why nothing is here and offer the next step.",
    demos=[
        ("First use", """
<div class="h-empty">
  <div class="h-empty__icon">%s</div>
  <h3 class="h-empty__title">No projects yet</h3>
  <p class="h-empty__body">Projects keep your tasks, files and people in one place. Create the first one to get started.</p>
  <div class="h-empty__actions">
    <button class="h-button h-button--bold">%s Create project</button>
    <button class="h-button h-button--subtle">Import from CSV</button>
  </div>
</div>""" % (I("folder"), I("plus")), {"bg": "raised"}),
        ("No results", """
<div class="h-empty">
  <div class="h-empty__icon">%s</div>
  <h3 class="h-empty__title">No matches for "aurora"</h3>
  <p class="h-empty__body">Check the spelling or try fewer filters.</p>
  <div class="h-empty__actions"><button class="h-button h-button--outline">Clear filters</button></div>
</div>""" % I("search"), {"bg": "raised"}),
    ],
    use=["Say what this space is for, then say how to fill it.", "Offer one clear primary action."],
    avoid=["Humor that makes a real problem feel small.", "Empty states with no action."],
)

add(
    id="accordion", title="Accordion", group="Display",
    blurb="Accordions reveal detail on demand. Built on the native details element.",
    demos=[
        ("Accordion", """
<div style="max-width:560px">
  <details class="h-accordion" open>
    <summary>What is Hali?</summary>
    <div class="h-accordion__body">A dark first design language built on Nord, with Atlassian structure and Material 3 tonal surfaces.</div>
  </details>
  <details class="h-accordion">
    <summary>Does it support light mode?</summary>
    <div class="h-accordion__body">Yes. Light is derived from dark and meets the same contrast targets.</div>
  </details>
  <details class="h-accordion">
    <summary>Can I override a component?</summary>
    <div class="h-accordion__body">Hali's CSS lives in cascade layers, so your unlayered styles always win.</div>
  </details>
</div>""", {}),
    ],
    a11y=["Native `details` and `summary` give keyboard and screen reader behavior for free."],
)

add(
    id="misc", title="Divider, key and code", group="Display",
    blurb="Small building blocks for documentation and dense interfaces.",
    demos=[
        ("Divider", """
<div class="h-stack h-gap-8" style="max-width:420px">
  <p>Above the line</p>
  <hr class="h-divider" style="margin:0">
  <p>Below the line</p>
</div>""", {}),
        ("Keyboard keys", """
<p>Press <kbd class="h-kbd">Ctrl</kbd> + <kbd class="h-kbd">K</kbd> to search, or <kbd class="h-kbd">Esc</kbd> to close.</p>""", {}),
        ("Code", """
<div class="h-stack" style="max-width:520px">
  <p>Use <code class="h-code">--hali-surface-raised</code> for cards.</p>
  <pre class="h-codeblock"><code>.card {
  background: var(--hali-surface-raised);
  border: 1px solid var(--hali-border-default);
  border-radius: var(--hali-radius-lg);
}</code></pre>
</div>""", {}),
    ],
)

# ---------------------------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------------------------

PATTERNS = []


def pattern(**kw):
    kw.setdefault("notes", [])
    PATTERNS.append(kw)


pattern(
    id="pattern-app", title="Application shell",
    blurb="The top bar, side navigation and a scrolling main area. This is the frame most Hali apps live in. On screens under 840px the side navigation hides, and your app swaps it for a menu button and a sheet.",
    height="600px",
    html="""
<div class="h-appshell h-appshell--contained">
  <header class="h-appshell__top h-topbar h-topbar--static">
    <a class="h-topbar__brand" href="#pattern-app">%s Hali</a>
    <div class="h-input-group" style="width:min(320px,40%%)">%s<input class="h-input h-input--sm" type="search" placeholder="Search" aria-label="Search"></div>
    <div class="h-topbar__actions">
      <button class="h-button h-button--subtle h-button--icon" aria-label="Help">%s</button>
      <button class="h-button h-button--subtle h-button--icon" aria-label="Notifications">%s</button>
      <span class="h-avatar h-accent-teal" role="img" aria-label="Your account">AR</span>
    </div>
  </header>
  <nav class="h-appshell__side h-sidenav" aria-label="Main">
    <a class="h-sidenav__item" href="#pattern-app" aria-current="page">%s Dashboard</a>
    <a class="h-sidenav__item" href="#pattern-app">%s Projects</a>
    <a class="h-sidenav__item" href="#pattern-app">%s Inbox <span class="h-badge h-is-danger">4</span></a>
    <a class="h-sidenav__item" href="#pattern-app">%s Reports</a>
    <div class="h-sidenav__section">Workspace</div>
    <a class="h-sidenav__item" href="#pattern-app">%s People</a>
    <a class="h-sidenav__item" href="#pattern-app">%s Settings</a>
  </nav>
  <main class="h-appshell__main">
    <div class="h-page">
      <nav aria-label="Breadcrumb"><ol class="h-breadcrumbs"><li><a href="#pattern-app">Workspace</a></li><li><span aria-current="page">Dashboard</span></li></ol></nav>
      <div class="h-page-header h-mt-16">
        <div>
          <h1 class="h-page-header__title">Good morning, Ana</h1>
          <p class="h-page-header__sub">Here is what changed across your projects.</p>
        </div>
        <div class="h-page-header__actions">
          <button class="h-button h-button--outline">%s Export</button>
          <button class="h-button h-button--bold">%s New project</button>
        </div>
      </div>
      <div class="h-grid" style="--h-col:180px">
        <div class="h-card"><div class="h-card__meta">Open tasks</div><div class="h-headline-md h-tabular h-mt-8">128</div><span class="h-lozenge h-is-success h-mt-8">%s 12%% this week</span></div>
        <div class="h-card"><div class="h-card__meta">In review</div><div class="h-headline-md h-tabular h-mt-8">23</div><span class="h-lozenge h-is-warning h-mt-8">%s 5 overdue</span></div>
        <div class="h-card"><div class="h-card__meta">Blocked</div><div class="h-headline-md h-tabular h-mt-8">4</div><span class="h-lozenge h-is-danger h-mt-8">%s Needs help</span></div>
      </div>
      <div class="h-table-wrap h-mt-24">
        <table class="h-table">
          <caption>Recent activity</caption>
          <thead><tr><th scope="col">Project</th><th scope="col">Status</th><th scope="col" data-numeric>Progress</th></tr></thead>
          <tbody>
            <tr><td>Aurora redesign</td><td><span class="h-lozenge h-is-brand">In progress</span></td><td data-numeric>64%%</td></tr>
            <tr><td>Billing migration</td><td><span class="h-lozenge h-is-warning">At risk</span></td><td data-numeric>38%%</td></tr>
            <tr><td>Mobile app</td><td><span class="h-lozenge h-is-success">Done</span></td><td data-numeric>100%%</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </main>
</div>""" % (MARK(), I("search"), I("help"), I("bell"), I("home"), I("folder"), I("inbox"), I("chart"), I("user"), I("sliders"), I("download"), I("plus"), I("arrow-right"), I("clock"), I("error")),
    notes=["Page width stops at 1120px so lines stay readable.",
           "Page padding is 16px on compact, 32px from 840px.",
           "Only the main area scrolls. The top bar and side navigation stay put."],
)

pattern(
    id="pattern-form", title="Form",
    blurb="Single column, labels above, one primary action. Validate on submit, then on blur once a field has been touched.",
    height="auto",
    html="""
<form class="h-card h-card--padded h-stack h-gap-24" style="max-width:520px" novalidate>
  <div>
    <h2 class="h-title-lg">Create workspace</h2>
    <p class="h-body-md h-text-subtle h-mt-8">Fields marked with an asterisk are required.</p>
  </div>
  <div class="h-field">
    <label class="h-label" for="pf-name" data-required>Workspace name</label>
    <input class="h-input" id="pf-name" value="Acme" aria-describedby="pf-name-help">
    <div class="h-help" id="pf-name-help">You can change this later in settings.</div>
  </div>
  <div class="h-field">
    <label class="h-label" for="pf-url" data-required>Workspace address</label>
    <input class="h-input" id="pf-url" value="acme corp" aria-invalid="true" aria-describedby="pf-url-err">
    <div class="h-error" id="pf-url-err">%s<span>Use letters, numbers and hyphens only. Try acme-corp.</span></div>
  </div>
  <fieldset class="h-fieldset">
    <legend>Plan</legend>
    <label class="h-check"><input type="radio" name="pf-plan" checked><span>Team, $8 per person each month</span></label>
    <label class="h-check"><input type="radio" name="pf-plan"><span>Business, $15 per person each month</span></label>
  </fieldset>
  <label class="h-switch"><input type="checkbox" role="switch" checked><span>Invite my team after setup</span></label>
  <div class="h-cluster" style="justify-content:flex-end">
    <button type="button" class="h-button h-button--subtle">Cancel</button>
    <button type="submit" class="h-button h-button--bold">Create workspace</button>
  </div>
</form>""" % I("error", "h-icon--sm"),
    notes=["Cancel is subtle, the primary action is bold, and both sit bottom right.",
           "On submit with errors, move focus to the first invalid field and summarize in an alert if there are many."],
)

pattern(
    id="pattern-delete", title="Destructive action",
    blurb="Prefer undo to confirmation. When an action cannot be undone, confirm with a dialog that names exactly what will be lost.",
    height="auto",
    html="""
<div class="h-stack h-gap-16" style="max-width:520px">
  <div class="h-alert h-is-danger" role="alert">
    %s
    <div>
      <div class="h-alert__title">Delete this workspace</div>
      <div class="h-alert__body">Deleting Acme removes 14 projects, 1,208 tasks and all files for 23 people. This cannot be undone.</div>
      <div class="h-alert__actions"><button class="h-button h-button--danger" data-dialog-open="dlg-ws">Delete workspace</button></div>
    </div>
  </div>
</div>
<dialog class="h-dialog h-dialog--sm" id="dlg-ws" aria-labelledby="dlg-ws-title">
  <div class="h-dialog__header"><h2 class="h-dialog__title" id="dlg-ws-title">Delete Acme?</h2></div>
  <div class="h-dialog__body h-stack">
    <p>Type <strong>Acme</strong> to confirm. Everyone loses access immediately.</p>
    <div class="h-field"><label class="h-label" for="dlg-ws-confirm">Workspace name</label><input class="h-input" id="dlg-ws-confirm" autocomplete="off"></div>
  </div>
  <div class="h-dialog__footer">
    <button class="h-button h-button--subtle" data-dialog-close>Cancel</button>
    <button class="h-button h-button--danger" data-dialog-close>Delete workspace</button>
  </div>
</dialog>""" % I("warning"),
)

pattern(
    id="pattern-settings", title="Settings list",
    blurb="Each row is one setting with a label, a short explanation and its control. Switches apply immediately.",
    height="auto",
    html="""
<div class="h-card h-card--padded" style="max-width:640px">
  <h2 class="h-title-lg">Notifications</h2>
  <div class="h-stack h-gap-0 h-mt-16">
    <div class="h-split" style="padding:16px 0;border-bottom:1px solid var(--hali-border-default)">
      <div><div class="h-label-lg">Email</div><div class="h-body-sm h-text-subtle">Daily summary of what changed</div></div>
      <label class="h-switch"><input type="checkbox" role="switch" checked aria-label="Email notifications"></label>
    </div>
    <div class="h-split" style="padding:16px 0;border-bottom:1px solid var(--hali-border-default)">
      <div><div class="h-label-lg">Push</div><div class="h-body-sm h-text-subtle">Mentions and direct messages</div></div>
      <label class="h-switch"><input type="checkbox" role="switch" aria-label="Push notifications"></label>
    </div>
    <div class="h-split" style="padding:16px 0">
      <div><div class="h-label-lg">Digest day</div><div class="h-body-sm h-text-subtle">When the weekly digest arrives</div></div>
      <div class="h-select" style="width:160px"><select aria-label="Digest day"><option>Monday</option><option>Friday</option></select>%s</div>
    </div>
  </div>
</div>""" % I("chevron-down"),
)

pattern(
    id="pattern-loading", title="Loading, empty and error",
    blurb="Every list has four states: loading, empty, error and populated. Design all four.",
    height="auto",
    html="""
<div class="h-grid" style="--h-col:260px">
  <div class="h-card">
    <div class="h-label-md h-text-subtle">Loading</div>
    <div class="h-stack h-gap-8 h-mt-12" aria-busy="true"><span class="h-sr-only" role="status">Loading</span><span class="h-skeleton h-skeleton--text"></span><span class="h-skeleton h-skeleton--text"></span><span class="h-skeleton h-skeleton--text" style="width:60%%"></span></div>
  </div>
  <div class="h-card">
    <div class="h-label-md h-text-subtle">Empty</div>
    <div class="h-empty" style="padding:24px 0 8px"><h3 class="h-empty__title">No comments yet</h3><p class="h-empty__body">Start the conversation.</p><div class="h-empty__actions"><button class="h-button h-button--outline h-button--sm">Add comment</button></div></div>
  </div>
  <div class="h-card">
    <div class="h-label-md h-text-subtle">Error</div>
    <div class="h-alert h-is-danger h-mt-12" role="alert" style="grid-template-columns:auto 1fr">%s<div><div class="h-alert__title">Could not load comments</div><div class="h-alert__actions"><button class="h-button h-button--sm h-button--outline">Try again</button></div></div></div>
  </div>
</div>""" % I("error"),
)

# ---------------------------------------------------------------------------------------------
# Content design
# ---------------------------------------------------------------------------------------------

VOICE_PRINCIPLES = [
    ("Clear", "Say the thing. One idea per sentence, plain words, no jargon the reader has not used themselves."),
    ("Calm", "Hali is quiet by design. No exclamation marks, no urgency theater, no jokes at the expense of a real problem."),
    ("Direct", "Lead with what the person needs to know or do. Put the reason second."),
    ("Human", "Write the way a capable colleague would talk. Use 'you' and 'we' sparingly and 'please' almost never."),
]

TONE_TABLE = [
    ("Success", "Brief and warm", "Project archived."),
    ("Neutral information", "Plain and short", "Your export will be ready in about two minutes."),
    ("Warning", "Specific and early", "Storage is 92% full. Free up space or upgrade before uploads stop."),
    ("Error", "Calm, helpful, never blaming", "We could not send the invite. Check the address and try again."),
    ("Destructive", "Serious and exact", "This deletes 14 projects and cannot be undone."),
    ("Empty", "Encouraging and practical", "No projects yet. Create one to get started."),
]

WRITING_RULES = [
    ("Sentence case", "Headings, buttons, labels and menu items use sentence case: 'Create project', not 'Create Project'. Proper nouns keep their capitals."),
    ("Buttons start with a verb", "Name the result: 'Save changes', 'Invite people', 'Delete project'. Avoid 'OK', 'Yes' and 'Submit'."),
    ("Confirm with the same words", "A dialog titled 'Delete project?' has a button that says 'Delete project'."),
    ("Errors say what happened and what to do", "Use the pattern: what went wrong, why if it helps, how to fix it. 'Enter a full address, like alex@acme.com.'"),
    ("Placeholders are examples, not labels", "Every field has a visible label. A placeholder shows a sample value and disappears on typing."),
    ("Numbers, dates and units", "Use digits. Write dates as 'Oct 17, 2026' and respect the person's locale. Put a space between number and unit: '16 MB'."),
    ("Avoid filler", "Cut 'Please', 'Simply', 'Just', 'Oops' and 'Sorry' unless something truly went wrong on our side."),
    ("Be inclusive", "Write about people, not about ability. Do not use idioms that do not translate. Do not rely on color words alone: 'the red button'."),
]

DO_DONT = [
    ("Save changes", "Submit"),
    ("We could not save your changes. Check your connection and try again.", "Oops! Something went wrong."),
    ("Delete 3 files? This cannot be undone.", "Are you sure?"),
    ("No results for 'aurora'. Try fewer filters.", "Nothing found."),
]

STATUS_TABLE = [
    ("Button, link, field, checkbox, radio, switch, segmented control, chip", "Stable", "1.0.0"),
    ("Lozenge, badge, dot, avatar, card, accordion, divider, kbd, code", "Stable", "1.0.0"),
    ("Alert, banner, toast, progress, spinner, skeleton, empty state", "Stable", "1.0.0"),
    ("Tabs, breadcrumbs, pagination, top bar, side navigation, rail", "Stable", "1.0.0"),
    ("Menu, dropdown, tooltip, dialog, side sheet", "Stable", "1.0.0"),
    ("Table with toolbar, sorting and selection styles", "Stable", "1.0.0"),
    ("Date picker, combobox, tree view, stepper, charts", "Planned", "after 1.0"),
]
