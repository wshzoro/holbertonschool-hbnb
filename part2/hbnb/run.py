"""
Main application entry point for the HBnB API server.
"""
from app import create_app
app = create_app()

if __name__ == '__main__':
    # Server configuration
    host = '0.0.0.0'  # Listen on all interfaces
    port = 5000
    debug = True
    
    print("\n" + "="*50)
    print("HBnB API Server")
    print("="*50)
    
    # Display available routes
    print("\nAvailable routes:")
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
        print(f"  {rule.rule} -> {rule.endpoint} [{methods}]")
    
    # Display important URLs (using 127.0.0.1 for clickable links in terminal)
    display_url = f"http://127.0.0.1:{port}"
    print("\nImportant URLs (clickable in terminal):")
    print(f"  Swagger UI:    {display_url}/ (redirige vers /api/v1/doc/")
    print(f"  Users API:     {display_url}/api/v1/users")
    print(f"  Amenities API: {display_url}/api/v1/amenities")
    print(f"  Health check:  {display_url}/health")
    
    print("\nConfiguration:")
    print(f"  Debug mode: {debug}")
    print(f"  Host: 0.0.0.0 (accessible from network)")
    print(f"  Port: {port}")
    
    print("\n" + "="*50)
    print("Starting server... (Press Ctrl+C to stop)")
    print("="*50 + "\n")
    
    # Start the development server
    app.run(host=host, port=port, debug=debug)
