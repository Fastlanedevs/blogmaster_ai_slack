
# Blogmaster AI 

Blogmaster AI is a Flask-based backend service that generates blog content using AI. It leverages the CrewAI framework to orchestrate a team of AI agents that plan, write, blogs by posting request on SLACK.

## Features

- Create blog posts on any given topic
- Customize content type, tonality, and content goal
- Asynchronous task processing
- RESTful API for task creation and status checking

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/realaman90/blogmaster_ai.git
   cd blogmaster-ai-backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   MONGO_DB_URI=your_mongodb_connection_string
   OPENAI_API_KEY='NA'
   SERPER_API_KEY=your_serper_api_key
   ```
---

**Note:** Ensure you us 'NA' for open AI key this will use local model running on ollama.

---
   
4. Install Ollama
    go to https://ollama.com/
    Install ollama 
    go to your terminal and run the following command
    ```
    ollama run llama3
    
    ```
    This will start the openai model on your local machine.



## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. The API will be available at `http://localhost:5000`

## API Endpoints

- `POST /create_task`: Create a new blog post task
  - Request body:
    ```json
    {
      "topic": "Your topic",
      "content_type": "blog",
      "tonality": "casual",
      "content_goal": "inform"
    }
    ```
  - Response: Task ID

- `GET /get_task_status/<task_id>`: Check the status of a task

- `GET /get_task_result/<task_id>`: Retrieve the completed blog post

## Architecture

The system uses a multi-agent approach with CrewAI:
1. Content Strategist and Researcher
2. Expert Content Creator
3. Senior Content Editor

These agents work together to plan, write, and refine the blog post based on the given parameters.

## Exposing the API

To make your API accessible from the internet, you can use a reverse proxy like Nginx. Here's how to set it up:

1. Install Nginx:
   ```
   sudo apt update
   sudo apt install nginx
   ```

2. Create a new Nginx configuration file:
   ```
   sudo nano /etc/nginx/sites-available/blogmaster
   ```

3. Add the following configuration:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```
   Replace `your_domain.com` with your actual domain name.

4. Create a symbolic link to enable the site:
   ```
   sudo ln -s /etc/nginx/sites-available/blogmaster /etc/nginx/sites-enabled/
   ```

5. Test the Nginx configuration:
   ```
   sudo nginx -t
   ```

6. If the test is successful, restart Nginx:
   ```
   sudo systemctl restart nginx
   ```
7. Map your domain to your server's IP address ( you can check it at `https://www.whatismyip.com/`) in your DNS settings available at your DNS Manager( Route53, Godaddy etc..).

Now add an A record with your domain name and IP address.

Now your API should be accessible at `http://your_domain.com`.

Note: Make sure to set up proper security measures, such as SSL/TLS encryption and API authentication, before exposing your API to the internet.

### Alternative: Ngrok (for temporary access)
If you need a quick, temporary solution for development or testing, you can use Ngrok:

1. Install Ngrok: https://ngrok.com/download

2. Run Ngrok to expose your local server:
   ```
   ngrok http 5000
   ```

3. Ngrok will provide a public URL that forwards to your local server.

Remember that Ngrok URLs are temporary and will change each time you restart Ngrok.

## Project Structure

- `app.py`: Main Flask application with API routes
- `create_blog.py`: Contains the CrewAI logic for blog creation
- `utils.py`: Utility functions for task management and database operations
- `requirements.txt`: List of Python dependencies

## Dependencies

- Flask
- CrewAI
- Langchain
- PyMongo
- Requests

## Configuration

The project uses environment variables for configuration. Make sure to set the following in your `.env` file:

- `MONGO_DB_URI`: MongoDB connection string
- `OPENAI_API_KEY`: Use 'NA' for local model
- `SERPER_API_KEY`: Serper API key for web searching

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
```