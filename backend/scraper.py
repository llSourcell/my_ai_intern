import asyncio
import subprocess
import json
import os
import tempfile
from config import get_config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_mcp_config(api_token, web_unlocker_zone=None, browser_auth=None):
    """Create a temporary MCP configuration file with Bright Data settings"""
    config = {
        "mcpServers": {
            "Bright Data": {
                "command": "npx",
                "args": ["@brightdata/mcp"],
                "env": {
                    "API_TOKEN": api_token
                }
            }
        }
    }
    
    if web_unlocker_zone:
        config["mcpServers"]["Bright Data"]["env"]["WEB_UNLOCKER_ZONE"] = web_unlocker_zone
    
    if browser_auth:
        config["mcpServers"]["Bright Data"]["env"]["BROWSER_AUTH"] = browser_auth
    
    temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(config, temp_config)
    temp_config.close()
    
    return temp_config.name

def run_mcp_scraper(prompt, config_path):
    """Run a Bright Data MCP scraping task using the MCP client"""
    try:
        cmd = ["npx", "@brightdata/mcp-client", "--config", config_path, "--prompt", prompt]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"MCP client error: {result.stderr}")
            return []
        
        # Parse the output to extract structured data
        try:
            # The output might contain logs and other information before the JSON
            # Look for a valid JSON object in the output
            output_lines = result.stdout.strip().split('\n')
            json_data = None
            
            for line in output_lines:
                line = line.strip()
                if line.startswith('{') and line.endswith('}'):
                    try:
                        json_data = json.loads(line)
                        break
                    except json.JSONDecodeError:
                        continue
            
            if json_data and 'agents' in json_data:
                return json_data['agents']
            elif json_data:
                return [json_data]
            else:
                logger.warning("No valid JSON data found in MCP output")
                return []
                
        except json.JSONDecodeError:
            logger.error(f"Failed to parse MCP output: {result.stdout}")
            return []
            
    except Exception as e:
        logger.error(f"Error running MCP client: {str(e)}")
        return []
    finally:
        # Clean up the temporary config file
        if os.path.exists(config_path):
            os.unlink(config_path)

def scrape_realtor_agents(location="Austin, TX", limit=30):
    """Scrape real estate agents from Realtor.com using Bright Data MCP"""
    config = get_config()
    api_token = config['BRIGHTDATA_API_TOKEN']
    web_unlocker_zone = config['BRIGHTDATA_WEB_UNLOCKER_ZONE']
    browser_auth = config.get('BRIGHTDATA_BROWSER_AUTH', '')
    
    if not api_token:
        logger.warning("No Bright Data API token provided. Using dummy data.")
        return generate_dummy_agents(location, limit)
    
    # Create MCP config file
    config_path = create_mcp_config(api_token, web_unlocker_zone, browser_auth)
    
    # Craft the prompt for agent extraction
    prompt = f"Extract data for {limit} real estate agents in {location} from Realtor.com. For each agent, get their name, phone number, brokerage name, address, and website if available. Return as structured JSON."
    
    # Run the MCP scraper
    agents = run_mcp_scraper(prompt, config_path)
    
    # Process and format the results
    formatted_agents = []
    for agent in agents[:limit]:
        formatted_agents.append({
            'name': agent.get('name', 'Unknown Agent'),
            'phone': agent.get('phone', 'N/A'),
            'category': 'Real Estate Agent',
            'address': agent.get('address', f'{location}'),
            'website': agent.get('website', '')
        })
    
    return formatted_agents

def scrape_zillow_agents(location="Austin, TX", limit=30):
    """Scrape real estate agents from Zillow using Bright Data MCP"""
    config = get_config()
    api_token = config['BRIGHTDATA_API_TOKEN']
    web_unlocker_zone = config['BRIGHTDATA_WEB_UNLOCKER_ZONE']
    browser_auth = config.get('BRIGHTDATA_BROWSER_AUTH', '')
    
    if not api_token:
        logger.warning("No Bright Data API token provided. Using dummy data.")
        return generate_dummy_agents(location, limit)
    
    # Create MCP config file
    config_path = create_mcp_config(api_token, web_unlocker_zone, browser_auth)
    
    # Craft the prompt for agent extraction
    prompt = f"Extract data for {limit} real estate agents in {location} from Zillow.com. For each agent, get their name, phone number, brokerage name, address, and website if available. Return as structured JSON."
    
    # Run the MCP scraper
    agents = run_mcp_scraper(prompt, config_path)
    
    # Process and format the results
    formatted_agents = []
    for agent in agents[:limit]:
        formatted_agents.append({
            'name': agent.get('name', 'Unknown Agent'),
            'phone': agent.get('phone', 'N/A'),
            'category': 'Real Estate Agent',
            'address': agent.get('address', f'{location}'),
            'website': agent.get('website', '')
        })
    
    return formatted_agents

def mine_social_media_for_buyers(location="Austin, TX", limit=20):
    """Mine social media for buyer intent signals using Bright Data MCP"""
    config = get_config()
    api_token = config['BRIGHTDATA_API_TOKEN']
    web_unlocker_zone = config['BRIGHTDATA_WEB_UNLOCKER_ZONE']
    browser_auth = config.get('BRIGHTDATA_BROWSER_AUTH', '')
    
    if not api_token:
        logger.warning("No Bright Data API token provided. Using dummy data.")
        return generate_dummy_buyers(location, limit)
    
    # Create MCP config file
    config_path = create_mcp_config(api_token, web_unlocker_zone, browser_auth)
    
    # Craft prompts for different platforms
    platforms = [
        {
            "name": "Reddit",
            "prompt": f"Find recent posts on Reddit where people are talking about moving to {location} or looking for housing in {location}. Extract their requirements, budget if mentioned, and any other relevant details. Return as structured JSON."
        },
        {
            "name": "Twitter",
            "prompt": f"Find recent tweets where people mention moving to {location}, looking for houses in {location}, or needing a real estate agent in {location}. Return as structured JSON."
        },
        {
            "name": "Facebook Groups",
            "prompt": f"Find housing or real estate focused Facebook groups for {location} and extract recent posts from people looking to buy or rent. Return as structured JSON."
        }
    ]
    
    all_buyers = []
    for platform in platforms:
        # Run the MCP scraper for each platform
        buyers = run_mcp_scraper(platform["prompt"], config_path)
        all_buyers.extend(buyers)
        
        # Recreate config file for each platform
        config_path = create_mcp_config(api_token, web_unlocker_zone, browser_auth)
    
    # Process and format the results
    formatted_buyers = []
    for buyer in all_buyers[:limit]:
        formatted_buyers.append({
            'platform': buyer.get('platform', 'Unknown'),
            'user_id': buyer.get('user_id', 'anonymous'),
            'post_content': buyer.get('content', ''),
            'location_interest': buyer.get('location', location),
            'requirements': buyer.get('requirements', ''),
            'budget': buyer.get('budget', 'Not specified'),
            'timestamp': buyer.get('timestamp', '')
        })
    
    return formatted_buyers

def match_buyers_to_agents(buyers, agents, location="Austin, TX"):
    """Match potential buyers with suitable real estate agents based on location and requirements"""
    matches = []
    
    for agent in agents:
        # Extract zip code from agent address if available
        agent_zip = extract_zip_from_address(agent['address']) or location
        
        matched_buyers = []
        for buyer in buyers:
            # Check if buyer's location interest matches agent's area
            if location_match(buyer['location_interest'], agent_zip):
                matched_buyers.append(buyer)
        
        if matched_buyers:
            matches.append({
                'agent': agent,
                'potential_buyers': matched_buyers,
                'buyer_count': len(matched_buyers)
            })
    
    # Sort matches by number of potential buyers (descending)
    matches.sort(key=lambda x: x['buyer_count'], reverse=True)
    
    return matches

def extract_zip_from_address(address):
    """Extract zip code from an address string"""
    # Simple implementation - would need to be more robust in production
    parts = address.split()
    for part in parts:
        if len(part) == 5 and part.isdigit():
            return part
    return None

def location_match(buyer_location, agent_location):
    """Check if buyer and agent locations match"""
    # Simple implementation - in production would use more sophisticated geo-matching
    return buyer_location.lower() in agent_location.lower() or agent_location.lower() in buyer_location.lower()

def generate_dummy_agents(location="Austin, TX", limit=30):
    """Generate dummy agent data when API key is not available"""
    dummy_agents = []
    brokerages = ["Century 21", "RE/MAX", "Keller Williams", "Coldwell Banker", "Sotheby's"]
    
    for i in range(limit):
        dummy_agents.append({
            'name': f"Agent Smith {i+1}",
            'phone': f"512-555-{1000+i}",
            'category': 'Real Estate Agent',
            'address': f"{100+i} Main St, {location}",
            'website': f"https://agent{i+1}.realtor.example.com"
        })
    
    return dummy_agents

def generate_dummy_buyers(location="Austin, TX", limit=20):
    """Generate dummy buyer data when API key is not available"""
    dummy_buyers = []
    platforms = ["Reddit", "Twitter", "Facebook"]
    requirements = [
        "3BR/2BA single family home",
        "Condo near downtown",
        "House with yard for dogs",
        "New construction in suburbs",
        "Townhouse with garage"
    ]
    
    for i in range(limit):
        platform = platforms[i % len(platforms)]
        requirement = requirements[i % len(requirements)]
        
        dummy_buyers.append({
            'platform': platform,
            'user_id': f"user{i+1}",
            'post_content': f"Looking to move to {location} soon. Need help finding a {requirement}.",
            'location_interest': location,
            'requirements': requirement,
            'budget': f"${300000 + (i * 50000)}",
            'timestamp': "2023-05-01"
        })
    
    return dummy_buyers

def scrape_real_estate_leads(location="Austin, TX", limit=30):
    """Main function to scrape real estate agents and match with potential buyers"""
    # Get agents from multiple sources
    realtor_agents = scrape_realtor_agents(location, limit//2)
    zillow_agents = scrape_zillow_agents(location, limit//2)
    
    # Combine agents from different sources
    all_agents = realtor_agents + zillow_agents
    
    # Mine social media for buyer intent signals
    buyers = mine_social_media_for_buyers(location, limit)
    
    # Match buyers with agents
    matches = match_buyers_to_agents(buyers, all_agents, location)
    
    # Return matched agents with buyer counts
    enhanced_agents = []
    for match in matches:
        agent = match['agent'].copy()
        agent['buyer_count'] = match['buyer_count']
        enhanced_agents.append(agent)
    
    # If we don't have enough matches, add remaining agents
    if len(enhanced_agents) < limit:
        for agent in all_agents:
            if agent not in [a for a in enhanced_agents]:
                agent['buyer_count'] = 0
                enhanced_agents.append(agent)
                if len(enhanced_agents) >= limit:
                    break
    
    return enhanced_agents[:limit]
