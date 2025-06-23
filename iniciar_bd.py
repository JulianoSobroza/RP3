# Use isso pra criar as tabelas do BD

from app import create_app, db
app = create_app()
with app.app_context():
    #try:
    db.create_all()
    print("Banco de dados criado com sucesso!")
    print(" =========> Tabelas criadas: " + ", ".join(table.name for table in db.metadata.sorted_tables))
    #except Exception as e:
    #    print(f"Erro ao criar o banco de dados: {e}")