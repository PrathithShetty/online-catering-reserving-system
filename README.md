# The Rasaganga — Online Catering Reservation & Ordering System

A full-stack web application that lets **The Rasaganga** (a South Indian vegetarian
restaurant on Outer Ring Road, Bellandur, Bangalore) publish its à la carte menu and
catering packages online and take event bookings from customers, while giving the
restaurant's staff a dashboard to manage packages, menus, and incoming orders.

This is the implementation of the "Online Catering Reserving and Ordering System" project
brief: an e-commerce style portal where an **admin/catering provider** manages what's for
sale and a **customer** browses, books, and tracks catering orders for their events.

---

## 1. What this project actually does

Two roles use the same site:

- **Customer** — creates an account, browses the full **Menu** (à la carte dishes,
  grouped by section, with real prices) or the **Catering Packages** grouped by occasion
  (Wedding, Birthday Party, Corporate Event, Festival), opens a package to see its menu
  and price per plate, books it for a specific event date and guest count, checks out
  (delivery address + phone), tracks the booking's status, and leaves a star rating +
  review once the order is completed.
- **Admin (catering provider)** — logs in to a separate dashboard, adds/edits/deletes
  catering packages, menu items (name, section, price, veg/non-veg, photo), and occasion
  categories, and reviews incoming bookings — moving each one from *Pending* →
  *Confirmed* / *Rejected* → *Completed*.

### Typical workflow

```
Customer:  Register/Login → Browse Menu or Packages → View Details & Price →
           Add to Cart (pick event date + guest count) → Checkout (address + phone) →
           Booking placed as "Pending" → Track status in "My Bookings" →
           Leave a review once "Completed"

Admin:     Login → Dashboard → Manage Categories / Menu Items / Packages →
           Review incoming bookings → Accept (Confirm) / Reject → Mark Completed
```

---

## 2. Tech stack, and why each piece was picked

| Layer | Choice | Why |
|---|---|---|
| Backend framework | **Django 6 (Python)** | Batteries-included: routing, ORM, auth, admin, forms, and templating all ship together, so a full booking/e‑commerce flow (accounts, cart, orders, file uploads) can be built without stitching together many small libraries. Its ORM maps directly onto the catalog/cart/order relational model this project needs. |
| Database | **SQLite** (dev) | Zero-setup, file-based (`db.sqlite3`), ships with Python/Django — ideal for a project like this that needs to run immediately on any machine. The same models work unchanged against MySQL/PostgreSQL later by just changing `DATABASES` in `settings.py`, matching the brief's "SQLite initially, then MySQL if needed". |
| Templating / Frontend | **Django Templates + Bootstrap 5 + Bootstrap Icons + Google Fonts** | Server-rendered HTML keeps the project simple (no separate JS build step / API layer needed for a booking site like this) while Bootstrap gives a responsive, mobile-friendly UI (the brief explicitly calls out managing the catalog "using a mobile device") without hand-writing a CSS framework. Playfair Display + Poppins (loaded in `base.html`) give the public pages an editorial, restaurant-menu feel on top of Bootstrap's grid. |
| Image handling | **Pillow** | Required by Django's `ImageField` (package photos, menu item photos, category photos) to validate and process uploaded images. |
| Auth | **Django's built-in auth, with a custom `User` model** | Avoids reinventing password hashing/session/login security; extended with a `role` field (`CUSTOMER` / `ADMIN`) so the same login system drives both the public site and the admin dashboard. |
| Admin/back-office | **A custom dashboard (`/dashboard/...`) + Django's built-in `/admin/`** | The custom dashboard is the day-to-day tool restaurant staff use (simple, Bootstrap-styled CRUD screens for packages/menu/orders). Django's built-in admin is kept too, as a lower-level power-user tool (useful for the developer / superuser). |

**Why this combination "helped"**: it let the whole project — accounts, catalog
management, cart, checkout, order-status workflow, and reviews — be built as *one*
Django project with a handful of small, focused apps, using only two third-party Python
packages (`Django`, `Pillow`). That keeps the codebase easy to read end-to-end and easy
to grade/demo, while still demonstrating the core full-stack skills the brief asks for:
authentication, CRUD, relational database design, an order/booking pipeline, and a
role-based dashboard.

---

## 3. Project structure

The repo is split into a **`backend/`** folder (all Python/Django code — the server,
the database, the business logic) and a **`frontend/`** folder (everything the browser
actually renders — HTML templates, CSS, images). Django is a server-rendered framework,
so "frontend" here means *presentation layer*, not a separate JS app — `backend/` reads
`frontend/templates` and `frontend/static` directly (wired up in
`backend/catering_system/settings.py`).

```
Online Catering Reserving/
├── venv/                        Python virtual environment (not committed)
├── README.md
├── .gitignore
├── .claude/launch.json          Tells the Claude Code preview tool how to start the dev
│                                 server (backend/manage.py runserver)
│
├── backend/                     ALL PYTHON / DJANGO CODE
│   ├── manage.py                 Django's command-line entry point (runserver, migrate, ...)
│   ├── requirements.txt          Python packages needed to run the project (Django, Pillow)
│   ├── db.sqlite3                The SQLite database file (created after running migrations)
│   ├── media/                    USER-UPLOADED / SEEDED IMAGES (package, menu item, category
│   │                             photos) — served only in development; excluded from git
│   │
│   ├── catering_system/          THE PROJECT PACKAGE (global configuration)
│   │   ├── settings.py            All Django settings: installed apps, database, where
│   │   │                          `frontend/templates` and `frontend/static` live, auth
│   │   │                          redirect URLs, custom User model
│   │   ├── urls.py                Top-level URL router — includes each app's urls.py
│   │   └── wsgi.py / asgi.py      Entry points used by real web servers to run the app
│   │
│   ├── accounts/                 APP: user accounts & authentication
│   │   ├── models.py              Custom `User` model (extends Django's AbstractUser) with
│   │   │                          `role` (CUSTOMER/ADMIN), `phone`, `address`
│   │   ├── forms.py               Sign-up form, profile-edit form, styled login form
│   │   ├── views.py               Login, logout, sign-up, "my profile" pages
│   │   ├── urls.py                /accounts/login/, /accounts/signup/, /accounts/profile/, ...
│   │   ├── decorators.py          `@admin_required` — guards every dashboard view so only
│   │   │                          staff/ADMIN-role users can reach it
│   │   └── admin.py               Registers the custom User model with Django's built-in admin
│   │
│   ├── catering/                 APP: the product catalog (what's for sale)
│   │   ├── models.py              `Category` (Wedding/Birthday/...), `MenuItem` (a dish —
│   │   │                          name, section, food type, veg flag, price, photo),
│   │   │                          `CateringPackage` (a bookable combo: price/plate, guest
│   │   │                          range, photo, linked menu items, category)
│   │   ├── forms.py               Admin-facing forms to create/edit categories, menu items,
│   │   │                          and packages
│   │   ├── views.py               Public pages (home, the Menu page, package list/search,
│   │   │                          package detail) AND the admin dashboard CRUD views for
│   │   │                          categories/menu items/packages
│   │   ├── urls.py                Public catalog routes + `/dashboard/...` management routes
│   │   ├── admin.py               Registers Category/MenuItem/CateringPackage with Django admin
│   │   └── management/commands/
│   │       └── seed_data.py       A custom `manage.py seed_data` command that wipes and
│   │                              re-creates The Rasaganga's real categories, à la carte
│   │                              menu (transcribed from the restaurant's own menu boards,
│   │                              with real prices), and catering packages — used to demo
│   │                              the site with realistic data instead of an empty database
│   │
│   └── orders/                   APP: cart, checkout, bookings, reviews
│       ├── models.py              `Cart` / `CartItem` (pre-checkout selections with event
│       │                          date & guest count), `Order` / `OrderItem` (a placed
│       │                          booking, with a status: Pending/Confirmed/Rejected/
│       │                          Completed/Cancelled), `Review` (star rating + comment on
│       │                          a package, tied to a completed order)
│       ├── forms.py               Add-to-cart form (event date, guests, special requests),
│       │                          checkout form (delivery address, phone), review form
│       ├── views.py               Cart management, checkout → creates an Order, "My
│       │                          Bookings", order detail/cancel, leaving a review, AND the
│       │                          admin dashboard's order list / status-update views
│       ├── urls.py                /orders/cart/, /orders/checkout/, /orders/my-orders/, ...
│       └── admin.py               Registers Cart/Order/Review with Django admin
│
└── frontend/                    EVERYTHING THE BROWSER RENDERS
    ├── templates/                 ALL HTML TEMPLATES (server-rendered by Django views)
    │   ├── base.html               Shared layout: navbar, messages, footer, Google Fonts —
    │   │                           every page extends this
    │   ├── accounts/               login.html, signup.html, profile.html
    │   ├── catering/
    │   │   ├── home.html, menu.html, package_list.html, package_detail.html  (public pages)
    │   │   └── dashboard/          base_dashboard.html + CRUD screens for packages, menu
    │   │                           items, categories, plus the dashboard home/overview
    │   └── orders/
    │       ├── cart.html, checkout.html, add_to_cart.html
    │       ├── my_orders.html, order_detail.html, add_review.html
    │       └── dashboard/order_manage_list.html   (admin's booking queue)
    │
    └── static/                    CSS/JS/images served as-is (not user-uploaded)
        ├── css/style.css            The Rasaganga's dark/gold editorial theme (navbar, hero,
        │                            occasion cards, package cards, the Menu page's layout)
        └── img/rasaganga/           Source photos (signage, storefront, food) used for the
                                     hero, "Visit Us" section, and Menu page section photos
```

---

## 4. How the pieces fit together (request flow)

1. `backend/catering_system/urls.py` receives every request and hands it to the right
   app's `urls.py` (`accounts/`, `catering/`, or `orders/`).
2. That app's `views.py` runs the actual logic — reading/writing the database through
   `models.py`, validating any submitted form via `forms.py`.
3. The view renders a template from `frontend/templates/`, which extends `base.html` and
   pulls in `frontend/static/css/style.css` for styling.
4. Anything the customer or admin uploads (package photos, menu item photos) is written
   to `backend/media/` and served back through the `<img>` tags in the templates.

---

## 5. Running it locally

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r backend/requirements.txt

python backend/manage.py migrate       # creates backend/db.sqlite3 with all tables
python backend/manage.py seed_data     # loads The Rasaganga's real menu/categories/packages
python backend/manage.py createsuperuser   # create an admin login (or reuse an existing one)

python backend/manage.py runserver
```

Then open `http://127.0.0.1:8000/`.

- Sign up as a normal visitor to use the **customer** flow (browse the Menu or Packages →
  book → checkout → track order).
- Log in with a superuser / `role=ADMIN` account to reach the **admin dashboard** at
  `/dashboard/` (manage packages, menu items, categories, and bookings) — the dashboard
  link only appears in the navbar for admin accounts.

## 6. Deploying to production (Vercel)

Locally this project uses SQLite and the local `backend/media/` folder — fine for
development, but Vercel's filesystem is **ephemeral** (nothing written to disk survives
between requests), so production needs a real external database and external file
storage. `settings.py` already supports both, switched on automatically by environment
variables — with none set, everything falls back to the exact local setup above.

| Piece | Local dev | Production |
|---|---|---|
| Database | SQLite file | Postgres (e.g. [Neon](https://neon.tech) or [Supabase](https://supabase.com), both have a free tier) via `DATABASE_URL` |
| Media (uploaded photos) | `backend/media/` | [Cloudinary](https://cloudinary.com) (free tier) via `CLOUDINARY_URL` |
| Static files (CSS/images) | served by `runserver` | served by [WhiteNoise](https://whitenoise.readthedocs.io/), bundled into the app |

**One-time setup:**

1. Create a free Postgres database (Neon or Supabase) and copy its connection string.
2. Create a free Cloudinary account and copy the `CLOUDINARY_URL` from its dashboard.
3. Push this repo to GitHub, then import it in Vercel ("Add New Project").
4. In Vercel's Project → Settings → Environment Variables, add: `DATABASE_URL`,
   `CLOUDINARY_URL`, `DJANGO_SECRET_KEY` (a long random string — see `.env.example` for
   how to generate one), `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` and
   `DJANGO_CSRF_TRUSTED_ORIGINS` (both set to your `*.vercel.app` domain once you know it).
5. Before or right after the first deploy, run migrations (and optionally `seed_data`)
   *against the production database* from your own machine:
   ```bash
   # with DATABASE_URL (and CLOUDINARY_URL) set in your local .env to the real values
   python backend/manage.py migrate
   python backend/manage.py seed_data
   python backend/manage.py createsuperuser
   ```
6. Deploy — either `vercel --prod` from the repo root, or via Vercel's GitHub integration
   on every push to `main`.

`.env.example` documents every variable above. Copy it to `.env` (already git-ignored)
for local testing against the real production database/media services before deploying.

## 7. Roadmap / natural next steps

- Real payment gateway integration at checkout (currently bookings are placed as
  "Pending" for the restaurant to confirm manually, with no online payment step).
- Email/SMS notifications when a booking's status changes.
- Letting a customer build a custom catering order directly from the à la carte **Menu**
  page (today the Menu page is browse-only; bookings go through curated Packages).
