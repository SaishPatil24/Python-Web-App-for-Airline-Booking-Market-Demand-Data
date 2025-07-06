import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import pandas as pd

load_dotenv(find_dotenv())

def generate_ai_summary(df, airport, hours_back):
    key = os.getenv("GROQ_API_KEY")
    
   
    if not key:
        current_dir = os.getcwd()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        env_path = os.path.join(parent_dir, '.env')
        
        print(f"DEBUG - Current working directory: {current_dir}")
        print(f"DEBUG - Script directory: {script_dir}")
        print(f"DEBUG - Parent directory: {parent_dir}")
        print(f"DEBUG - Looking for .env at: {env_path}")
        print(f"DEBUG - .env exists: {os.path.exists(env_path)}")
        
        if os.path.exists(env_path):
            load_dotenv(env_path)
            key = os.getenv("GROQ_API_KEY")
            print(f"DEBUG - After explicit load, key found: {key is not None}")
        
        if not key:
            cwd_env = os.path.join(current_dir, '.env')
            if os.path.exists(cwd_env):
                load_dotenv(cwd_env)
                key = os.getenv("GROQ_API_KEY")
                print(f"DEBUG - After CWD load, key found: {key is not None}")
    
    if not key:
        
        debug_info = f"""
❌ Groq API Key not configured.

Debug Information:
- Current working directory: {os.getcwd()}
- Script location: {os.path.dirname(os.path.abspath(__file__))}
- All environment variables with 'GROQ': {[k for k in os.environ.keys() if 'GROQ' in k.upper()]}
- .env file paths checked:
  - {os.path.join(os.getcwd(), '.env')} (exists: {os.path.exists(os.path.join(os.getcwd(), '.env'))})
  - {os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')} (exists: {os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))})

Solutions:
1. Make sure your .env file is in the project root (same directory as app.py)
2. Restart your Streamlit app completely
3. Try adding the API key directly to your system environment
        """
        return debug_info
    
    
    if df is None or df.empty:
        return "❌ No flight data available for analysis."
    
    
    required_columns = ["departure", "arrival", "departure_time", "arrival_time"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return f"❌ Missing required columns: {', '.join(missing_columns)}"
    
    
    try:
        
        total_flights = len(df)
        
       
        routes = df.groupby(['departure', 'arrival']).size().reset_index(name='count')
        top_routes = routes.nlargest(5, 'count')
        
       
        if df['departure_time'].dtype == 'object':
            df['departure_time'] = pd.to_datetime(df['departure_time'], errors='coerce')
        if df['arrival_time'].dtype == 'object':
            df['arrival_time'] = pd.to_datetime(df['arrival_time'], errors='coerce')
        
        
        df['departure_hour'] = df['departure_time'].dt.hour
        peak_hours = df['departure_hour'].value_counts().head(3)
        
       
        data_summary = f"""
Total Flights: {total_flights}

Top Routes:
{top_routes.to_string(index=False)}

Peak Hours (by departures):
{peak_hours.to_string()}

Sample Data:
{df[required_columns].head(3).to_string(index=False)}
        """
        
    except Exception as e:
        # Fallback to basic preview if data processing fails
        data_summary = f"""
Total Flights: {len(df)}
Sample Data:
{df[required_columns].head(5).to_string(index=False)}
        """
    
    prompt = f"""
You are an aviation market analyst.

Analyze flight traffic for airport **{airport}** over the past **{hours_back} hours**.

Flight Data Analysis:
{data_summary}

Please provide:
- ✈️ Most frequent routes (departure → arrival)
- 🕓 Peak traffic periods
- 📈 Travel demand trend (increasing, stable, or decreasing)
- 💡 Business recommendation (e.g. best routes to invest in hospitality or travel)

Be concise and insightful.
"""

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are an aviation market analyst with expertise in flight traffic analysis and business insights."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                          json=payload, headers=headers, timeout=30)
        res.raise_for_status()
        
        response_data = res.json()
        if 'choices' not in response_data or not response_data['choices']:
            return "❌ Invalid response format from Groq API"
            
        return response_data["choices"][0]["message"]["content"]
        
    except requests.exceptions.Timeout:
        return "❌ Request timeout - API took too long to respond"
    except requests.exceptions.HTTPError as e:
        return f"❌ HTTP Error from Groq API: {e.response.status_code} - {e.response.text if hasattr(e.response, 'text') else ''}"
    except requests.exceptions.RequestException as e:
        return f"❌ Network error: {e}"
    except KeyError as e:
        return f"❌ Unexpected response format: missing {e}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"