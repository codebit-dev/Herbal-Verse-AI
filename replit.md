# Virtual Herbal Garden - AYUSH Medicinal Plants Platform

## Overview
A comprehensive web-based virtual herbal garden platform that provides immersive learning about AYUSH (Ayurveda, Yoga & Naturopathy, Unani, Siddha, and Homeopathy) medicinal plants through 3D visualization, AI-powered tools, and integrated e-commerce functionality.

## Project Goals
- Educate users about traditional medicinal plants used in Ayurveda and AYUSH systems
- Provide interactive 3D visualization of medicinal plants
- Offer AI-powered plant identification and expert guidance
- Enable purchase of authentic Ayurvedic products
- Build a community platform for knowledge sharing

## Current State
The application is fully functional with the following features implemented:
- Interactive virtual garden with plant database
- 3D plant viewer using Three.js
- AI chatbot for Ayurveda questions (powered by OpenAI)
- Plant recognition through image upload
- E-commerce shop with Stripe payment integration
- Community portal for submitting plant information
- Admin dashboard for content moderation and analytics

## Recent Changes
- **October 31, 2025**: Initial project setup and development
  - Created Flask backend with SQLite database
  - Implemented all core features
  - Integrated OpenAI for AI chatbot and plant recognition
  - Integrated Stripe for payment processing with Stripe.js payment elements
  - Built responsive frontend with Bootstrap 5
  - Seeded database with 6 AYUSH medicinal plants
  - Created admin dashboard with HTTP Basic Authentication
  - Added secure payment flow with Payment Intents API
  - Implemented proper admin access control

## Project Architecture
Based on the provided architecture diagram:
- **User Layer**: Login/signup, search, upload images, chat with AI
- **Auth Service**: User authentication (planned for future)
- **User Dashboard**: Central hub connecting all features
- **Features**:
  - Plant Recognition Model (AI-powered image identification)
  - AI Chatbot (OpenAI-based Ayurveda expert)
  - Community Portal (user submissions with approval workflow)
  - Shop & Orders (e-commerce with Stripe)
  - AR/VR Garden Viewer (3D plant visualization with Three.js)
- **Herbal Database**: SQLite database storing plant information
- **Admin Dashboard**: Content moderation, analytics, and insights
- **Payment Gateway**: Stripe integration for secure payments

## Technology Stack
### Backend
- Flask 3.0.0 (Python web framework)
- SQLite (Database)
- OpenAI API (AI chatbot and image recognition)
- Stripe API (Payment processing)
- Flask-CORS (Cross-origin resource sharing)

### Frontend
- Bootstrap 5.3.0 (UI framework)
- Three.js (3D visualization)
- Vanilla JavaScript
- Font Awesome 6.4.0 (Icons)
- Custom CSS with nature-themed design

## Database Schema
### Plants
- id, name, scientific_name, category, overview, medicinal_uses, cultivation, image_url, model_url, created_at

### Products
- id, name, description, price, image_url, plant_id, stock, created_at

### Orders
- id, customer_name, customer_email, total_amount, items, stripe_payment_id, status, created_at

### Community Submissions
- id, plant_name, scientific_name, description, submitted_by, submitted_email, image_path, status, created_at

### Analytics
- id, event_type, event_data, created_at

## Environment Variables
**Required for Production:**
- `SESSION_SECRET`: **CRITICAL** - Secure random string for Flask session management (auto-generated in development, MUST be set in production)
- `STRIPE_SECRET_KEY`: Stripe secret key for payment processing
- `STRIPE_PUBLISHABLE_KEY`: Stripe publishable key for Stripe.js payment elements

**Required for Production:**
- `ADMIN_USERNAME`: Admin dashboard username (auto-generated securely if not set)
- `ADMIN_PASSWORD`: Admin dashboard password (auto-generated securely if not set)

**Optional:**
- `OPENAI_API_KEY`: For AI chatbot and plant recognition features (gracefully degrades if not set)

**Security Notes:**
- `SESSION_SECRET` must be a cryptographically secure random string in production
  - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
  - Without proper `SESSION_SECRET`, all session-based security can be bypassed
- `ADMIN_USERNAME` and `ADMIN_PASSWORD` are auto-generated with secure random values if not set
  - Auto-generated credentials are displayed in console on startup
  - For production, set these explicitly to known values
- All three secrets (SESSION_SECRET, ADMIN_USERNAME, ADMIN_PASSWORD) must be properly configured for production deployments

## API Endpoints
- `GET /`: Homepage
- `GET /garden`: Virtual garden with plant listings
- `GET /plant/<id>`: Individual plant details with 3D viewer
- `GET /shop`: Product catalog
- `GET /checkout`: Checkout page
- `GET /chatbot`: AI chatbot interface
- `GET /recognize`: Plant recognition page
- `GET /community`: Community portal
- `GET /admin`: Admin dashboard
- `POST /api/cart`: Manage shopping cart
- `POST /api/chat`: AI chatbot queries
- `POST /api/recognize-plant`: Plant image recognition
- `POST /api/submit-plant`: Submit new plant to community
- `POST /api/complete-order`: Complete purchase
- `POST /api/admin/approve-submission/<id>`: Approve community submission
- `POST /api/admin/reject-submission/<id>`: Reject community submission
- `GET /api/analytics`: Get analytics data

## Sample Plants in Database
1. **Ashwagandha** (Withania somnifera) - Adaptogen
2. **Tulsi** (Ocimum sanctum) - Immunity Booster
3. **Neem** (Azadirachta indica) - Purifier
4. **Brahmi** (Bacopa monnieri) - Brain Tonic
5. **Turmeric** (Curcuma longa) - Anti-inflammatory
6. **Amla** (Phyllanthus emblica) - Vitamin C Source

## User Preferences
- Clean, professional code structure
- Nature-themed UI with green color palette
- Mobile-responsive design
- Focus on educational content
- Authentic Ayurvedic information

## Future Enhancements (Next Phase)
- User authentication system with profiles and order history
- Advanced AR/VR viewing capabilities for immersive learning
- Complete admin approval workflow automation
- Advanced analytics and reporting dashboard
- Personalized plant recommendations based on health conditions
- Multi-language support for wider accessibility
- Enhanced 3D models with more detailed plant structures
- Integration with more payment providers
- Email notifications for orders and submissions
- Advanced search and filtering options

## Development Notes
- Flask runs on port 5000
- All routes are configured for the Replit environment
- OpenAI API used for chatbot (GPT-3.5-turbo) and image recognition (GPT-4o)
- Database is automatically initialized and seeded on startup
- Uploads are stored in the `uploads/` directory
- All plant images and 3D models are placeholders (SVG icons) for now
