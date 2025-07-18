#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta
from src.models.user import db, User, SportEvent, Market, Odd
from src.main import app

def seed_database():
    with app.app_context():
        # Limpar dados existentes
        db.drop_all()
        db.create_all()
        
        print("Criando usuário de teste...")
        # Criar usuário de teste
        user = User(username='teste', email='teste@armeiro.bet')
        user.set_password('123456')
        user.balance = 1000.0
        db.session.add(user)
        
        print("Criando eventos esportivos...")
        # Criar eventos esportivos
        events = [
            {
                'name': 'Flamengo vs Palmeiras',
                'sport': 'Futebol',
                'start_time': datetime.utcnow() + timedelta(hours=2)
            },
            {
                'name': 'Corinthians vs São Paulo',
                'sport': 'Futebol', 
                'start_time': datetime.utcnow() + timedelta(hours=4)
            },
            {
                'name': 'Lakers vs Warriors',
                'sport': 'Basquete',
                'start_time': datetime.utcnow() + timedelta(hours=6)
            },
            {
                'name': 'Real Madrid vs Barcelona',
                'sport': 'Futebol',
                'start_time': datetime.utcnow() + timedelta(days=1)
            }
        ]
        
        for event_data in events:
            event = SportEvent(**event_data)
            db.session.add(event)
            db.session.flush()  # Para obter o ID
            
            # Criar mercados para cada evento
            markets_data = [
                {'name': 'Resultado Final', 'odds': [
                    {'outcome': 'Casa', 'value': 2.1},
                    {'outcome': 'Empate', 'value': 3.2},
                    {'outcome': 'Fora', 'value': 2.8}
                ]},
                {'name': 'Total de Gols', 'odds': [
                    {'outcome': 'Mais de 2.5', 'value': 1.8},
                    {'outcome': 'Menos de 2.5', 'value': 2.0}
                ]}
            ]
            
            if event.sport == 'Basquete':
                markets_data = [
                    {'name': 'Resultado Final', 'odds': [
                        {'outcome': 'Casa', 'value': 1.9},
                        {'outcome': 'Fora', 'value': 1.9}
                    ]},
                    {'name': 'Total de Pontos', 'odds': [
                        {'outcome': 'Mais de 210.5', 'value': 1.85},
                        {'outcome': 'Menos de 210.5', 'value': 1.95}
                    ]}
                ]
            
            for market_data in markets_data:
                market = Market(
                    event_id=event.id,
                    name=market_data['name']
                )
                db.session.add(market)
                db.session.flush()
                
                for odd_data in market_data['odds']:
                    odd = Odd(
                        market_id=market.id,
                        outcome=odd_data['outcome'],
                        value=odd_data['value']
                    )
                    db.session.add(odd)
        
        db.session.commit()
        print("Banco de dados populado com sucesso!")
        print("Usuário de teste: teste / 123456")
        print("Saldo inicial: R$ 1000,00")

if __name__ == '__main__':
    seed_database()

