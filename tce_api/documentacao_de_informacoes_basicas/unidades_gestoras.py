from tce_api.base import Base
from itertools import repeat
from datetime import datetime
from models.unidade_gestora import UnidadeGestora
from models.municipio import Municipio
import pdb
class UnidadesGestoras(Base):
    def __init__(self):
        super().__init__()
        self.initialize_variables_by_method('unidades_gestoras')

    def execute(self):
        try:
            for municipio in Municipio.by_id_range(self.municipio_id):
                self.municipio_id = municipio.id
                unidades_gestoras = []
                for year in range(self.year, datetime.now().year):
                    self.year = year
                    response = self.request_tce_api(self.url_with_params(municipio.codigo, year))
                    response = self.sanitize_response(response.text)
                    for params in response['rsp']['_content']:
                        unidades_gestoras.append(UnidadeGestora(params))
                        UnidadeGestora.save_multiple(unidades_gestoras)
            self.save_progress('', True)
        except Exception as e:
            self.save_progress(e, False)

    def url_with_params(self, codigo, year):
        return ('?codigo_municipio=' + codigo + '&exercicio_orcamento=' + str(year))