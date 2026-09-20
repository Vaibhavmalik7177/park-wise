PARK-WISE: SMART PARKING AND VISITOR MANAGEMENT SYSTEM
Video Demo: https://youtu.be/lWrxvM_gW98?si=Gdk-ab6upN0e7MvX
Description:
I built Park-Wise to solve a very practical problem faced by many gated residential societies and apartment complexes: messy, manual visitor parking management. In most housing societies, the security gate still relies on physical pen-and-paper logbooks to track guest vehicles. From my experience seeing this system in action, it breaks down constantly. Handwriting is often impossible to read, entry times are guessed or written down incorrectly, logs get misplaced, and if a guest double-parks or blocks someone's driveway, finding their phone number means flipping through dozens of pages while traffic backs up at the gate, and in most of the small societies there are no gates where usually a person parks his car blocking driveway of others.
Park-Wise digitalizes this entire process into a web platform designed with two clean, role-specific portals: one for Visitors and one for Residents. The goal was to build a system that keeps visitor entry fast and simple for guests while giving residents the security tools they need to look up owner details instantly.
Key Features
 * Dual-Role Navigation System:
   * Visitor Portal: Guests can quickly register their account, log their vehicle registration number, set their estimated exit time, and view their active parking logs.
   * Resident Portal: Residents get full visibility over all active visitor traffic in the society, along with a dedicated search tool to look up vehicle owners during parking disputes.
 * Smart Vehicle Entry & Time Tracking:
   When visitors log an entry, the backend automatically records their exact arrival time in Indian Standard Time (IST). Guests only need to select their expected departure time. To keep data accurate, the application enforces real-time validation so past dates or invalid timestamps cannot be submitted.
 * Case-Insensitive Contact Lookup ("Find Number"):
   If a guest vehicle is blocking a resident's spot, the resident can enter the license plate into the lookup tool. To make this forgiving for everyday typing, I implemented SQL's COLLATE NOCASE operator and added string stripping in Python. Whether a resident types up14cv7177 or UP 14 CV 7177, the system matches the query correctly and displays the guest's contact number immediately.
 * Dynamic Error & Layout Handling:
   Borrowing dynamic design patterns from CS50's Finance project, errors are passed through a custom apology() renderer. I designed the error handler to check the active user session so that if something goes wrong, the error page renders inside the correct navigation bar and styling theme depending on whether a visitor or a resident is logged in.
How the Files Are Structured
Here is a breakdown of how I organized the codebase:
 * app.py: This serves as the main Flask backend. It handles all routing, processes form submissions, manages user session states, runs SQL queries, and enforces server-side validation.
 * helpers.py: Holds utility functions and decorators. This includes the @login_required wrapper used to secure private routes and the apology() helper used to render error messages cleanly.
 * parkwise.db: The SQLite database holding three primary tables (visitor_ids, resident, and visitor_log).
 * templates/:
  * ​apology.html: Renders custom error messages dynamically whenever backend validations fail or invalid actions are attempted.
  * ​checkmyvehicle.html: Allows logged-in visitors to view their active parking logs and current session status.
  * ​find_number.html & find_number_represe...: Search tools for residents to query vehicle registration numbers and instantly fetch visitor contact      details.
  * ​forgotpass_visitor.html & fprv.html: Dedicated password recovery pages allowing visitors to reset credentials without logging in.
  * ​history_vis_res.html: Master log view listing past and active parking records across both portals.
  * ​index_resident.html & index_visitor.html: The main dashboards for resident and visitor portals respectively.
  * ​layout_resident.html & layout_visitor.html: Base Jinja templates defining navigation bars, headers, and footer layouts tailored to each user role.
​  * login_resident.html & login_visitor.html: Portal-specific authentication forms.
  * ​register.html: New user registration form.
  * ​setting.html & setting_visitor.html: Account management pages where logged-in residents and visitors can access account preferences.
  * ​updatepaasv.html: Handles password changes for Non-logged-in users.
 * static/: Holds custom CSS (styles.css) for UI layout tweaks, card styling, and overall layout polish.
Database Architecture
I chose SQLite to keep the database lightweight and fast. The schema consists of three interconnected tables:
 * visitor_ids Table: Stores guest account profiles.
   * id: INTEGER PRIMARY KEY AUTOINCREMENT
   * username: TEXT NOT NULL UNIQUE
   * hash: TEXT NOT NULL
   * regno: TEXT NOT NULL
   * phone: TEXT NOT NULL
 * resident Table: Stores resident account details.
   * id: INTEGER PRIMARY KEY AUTOINCREMENT
   * username: TEXT NOT NULL UNIQUE
   * hash: TEXT NOT NULL
 * visitor_log Table: Tracks vehicle entries and exit logs.
   * id: INTEGER PRIMARY KEY AUTOINCREMENT
   * regisitration_no: TEXT NOT NULL
   * timein: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   * etime: TEXT NOT NULL
   * visitor_id: INTEGER (Foreign key referencing visitor_ids(id))
Bugs I Faced & Design Choices
Building this project came with a few tricky bugs that taught me a lot about databases and web development:
 * Resolving Database Constraint Crashes:
   Early on, I ran into an issue where saving a second log entry for the same user crashed the server with UNIQUE constraint failed: visitor_log.id. I realized I was trying to store the user's session ID directly inside the table's primary key id column. I fixed this by restructuring the schema so visitor_log.id uses auto-incrementing primary keys, and placed the user reference inside a dedicated visitor_id foreign key column instead.
 * Handling Timezone Discrepancies:
   Since development took place inside cloud containers running on UTC time, initial database timestamps were offset by 5 hours and 30 minutes from local Indian Standard Time (IST). I fixed this on the backend in Python by manualy adding 5-hour 30-minute using timedelta() before writing to SQLite, ensuring the arrival history always displays the exact local time.
 * Preventing Past-Date Entries:
   Allowing users to select past dates for future exit times made no sense. I fixed this by binding the HTML <input type="datetime-local"> min attribute dynamically using formatted ISO strings (YYYY-MM-DDTHH:MM), while also adding a backend fallback in Python to reject any timestamp earlier than current time.
Acknowledgments & References
 * CS50x (Harvard University): Design concepts for session management, dynamic apology rendering, and SQLite integration were referenced from the CS50 Finance problem set structure.
 * Gemini (Google AI): Used as a technical sounding board for debugging SQL constraint errors, fixing timezone calculations, and refining documentation.
