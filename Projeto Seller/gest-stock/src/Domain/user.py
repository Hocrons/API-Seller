class UserDomain:
    def __init__(self, id, name, email, password, status, celular, cnpj):
        self.id = id
        self.name = name
        self.email = email
        self.celular = celular
        self.cnpj = cnpj
        self.password = password
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "status": self.status,
            "celular": self.celular,
            "cnpj": self.cnpj,
            "status": self.status
        }
        
