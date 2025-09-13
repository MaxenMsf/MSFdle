#!/usr/bin/env python3
"""
Test des tags pour Agent Venom
"""
import sqlite3

def test_agent_venom():
    conn = sqlite3.connect('../data/msfdle.db')
    cursor = conn.cursor()
    
    # Test Agent Venom
    cursor.execute("""
        SELECT c.id, c.character_id, c.alias, GROUP_CONCAT(t.name, ', ') as tags
        FROM characters c
        LEFT JOIN character_tags ct ON c.id = ct.character_id
        LEFT JOIN tags t ON ct.tag_id = t.id
        WHERE c.character_id = 'AgentVenom'
        GROUP BY c.id
    """)
    
    result = cursor.fetchone()
    if result:
        print(f"Agent Venom: ID={result[0]}, character_id={result[1]}, alias={result[2]}, tags={result[3]}")
    else:
        print("Agent Venom non trouvé")
    
    # Test quelques autres personnages
    test_chars = ['AgathaHarkness', 'AdamWarlock', 'AmericaChavez']
    
    for char_id in test_chars:
        cursor.execute("""
            SELECT c.alias, GROUP_CONCAT(t.name, ', ') as tags
            FROM characters c
            LEFT JOIN character_tags ct ON c.id = ct.character_id
            LEFT JOIN tags t ON ct.tag_id = t.id
            WHERE c.character_id = ?
            GROUP BY c.id
        """, (char_id,))
        
        result = cursor.fetchone()
        if result:
            print(f"{result[0]}: {result[1] if result[1] else 'AUCUN'}")
    
    conn.close()

if __name__ == "__main__":
    test_agent_venom()