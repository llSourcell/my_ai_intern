import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import get_db, init_db
from scraper import scrape_lash_salons
from voice import place_call, get_llm_response
from config import get_config, save_config

app = Flask(__name__)
CORS(app)

# --- INIT DB (moved to first request handler) ---
@app.before_request
def setup():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

@app.route('/')
def index():
    return {'status': 'LeadGen API running'}

# --- Leads CRUD ---
@app.route('/api/leads', methods=['GET'])
def get_leads():
    with get_db() as conn:
        leads = conn.execute('SELECT * FROM leads').fetchall()
        return jsonify([dict(row) for row in leads])

@app.route('/api/leads', methods=['POST'])
def add_lead():
    data = request.json
    with get_db() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO leads (name, phone, category, address, website, status) VALUES (?, ?, ?, ?, ?, ?)''',
                  (data['name'], data['phone'], data['category'], data['address'], data.get('website', ''), data.get('status', 'Not Called')))
        conn.commit()
        return {'id': c.lastrowid}, 201

@app.route('/api/leads/<int:lead_id>', methods=['PATCH'])
def update_lead(lead_id):
    data = request.json
    with get_db() as conn:
        fields = []
        values = []
        for k in ['name', 'phone', 'category', 'address', 'website', 'status']:
            if k in data:
                fields.append(f"{k} = ?")
                values.append(data[k])
        if not fields:
            return {'error': 'No fields to update'}, 400
        values.append(lead_id)
        conn.execute(f"UPDATE leads SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
        return {'status': 'updated'}

@app.route('/api/scrape', methods=['POST'])
def scrape_new_leads():
    config = get_config()
    # If missing keys, return dummy data
    if not config['TWILIO_ACCOUNT_SID'] or not config['ELEVENLABS_API_KEY'] or not config['LLM_API_KEY']:
        dummy = [
            {'name': f'Lash Salon {i+1}', 'phone': f'555-000{i+1}', 'category': 'Lash Salon', 'address': f'{i+1} Main St, NYC', 'website': ''}
            for i in range(10)
        ]
        with get_db() as conn:
            c = conn.cursor()
            new_ids = []
            for lead in dummy:
                c.execute('''INSERT INTO leads (name, phone, category, address, website, status) VALUES (?, ?, ?, ?, ?, ?)''',
                          (lead['name'], lead['phone'], lead['category'], lead['address'], lead.get('website', ''), 'Not Called'))
                new_ids.append(c.lastrowid)
            conn.commit()
        return {'inserted_ids': new_ids, 'count': len(new_ids), 'dummy': True}
    # Real scrape
    limit = request.json.get('limit', 30)
    scraped = scrape_lash_salons(limit=limit)
    with get_db() as conn:
        c = conn.cursor()
        new_ids = []
        for lead in scraped:
            c.execute('''INSERT INTO leads (name, phone, category, address, website, status) VALUES (?, ?, ?, ?, ?, ?)''',
                      (lead['name'], lead['phone'], lead['category'], lead['address'], lead.get('website', ''), 'Not Called'))
            new_ids.append(c.lastrowid)
        conn.commit()
    return {'inserted_ids': new_ids, 'count': len(new_ids)}

@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    if request.method == 'GET':
        return jsonify(get_config())
    else:
        data = request.json or {}
        save_config(data)
        return {'status': 'updated'}

# --- Call Logs ---
@app.route('/api/call_logs', methods=['POST'])
def add_call_log():
    data = request.json
    with get_db() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO call_logs (lead_id, call_status, transcript) VALUES (?, ?, ?)''',
                  (data['lead_id'], data['call_status'], data.get('transcript', '')))
        conn.commit()
        return {'id': c.lastrowid}, 201

@app.route('/api/call_logs/<int:lead_id>', methods=['GET'])
def get_call_logs(lead_id):
    with get_db() as conn:
        logs = conn.execute('SELECT * FROM call_logs WHERE lead_id = ? ORDER BY created_at DESC', (lead_id,)).fetchall()
        return jsonify([dict(row) for row in logs])

@app.route('/api/call', methods=['POST'])
def call_lead():
    data = request.json
    lead_id = data['lead_id']
    script = data.get('script', "Hello, this is an introductory call from Lash Salon Leads. May I speak to the owner?")
    config = get_config()
    # Dummy mode
    if not config['TWILIO_ACCOUNT_SID'] or not config['ELEVENLABS_API_KEY'] or not config['LLM_API_KEY']:
        with get_db() as conn:
            conn.execute('UPDATE leads SET status = ? WHERE id = ?', ("Calling", lead_id))
            conn.commit()
        return {'call_sid': 'dummy-call', 'dummy': True}
    # Real mode
    with get_db() as conn:
        lead = conn.execute('SELECT * FROM leads WHERE id = ?', (lead_id,)).fetchone()
        if not lead:
            return {'error': 'Lead not found'}, 404
        try:
            call_sid = place_call(lead['phone'], script)
            conn.execute('UPDATE leads SET status = ? WHERE id = ?', ("Calling", lead_id))
            conn.commit()
            return {'call_sid': call_sid}
        except Exception as e:
            return {'error': str(e)}, 500

if __name__ == '__main__':
    import sys
    port = 5000
    if len(sys.argv) > 1 and sys.argv[1].startswith('--port'):
        try:
            port = int(sys.argv[1].split('=')[1])
        except Exception:
            port = 5001
    else:
        port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
