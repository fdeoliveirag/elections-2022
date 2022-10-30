"""
Resultados das Eleições 2022 - Presidência (1º Turno)

- API:         https://resultados.tse.jus.br/
- Ambiente:    oficial
- Ciclo:       ele2022
- Eleição:     544
- Pasta:       dados-simplificados
- Abrangência: br
- Cargo:       0001
- Arquivo:     r (resultados)

"""
import requests
import json
import time
import pandas as pd

URL        = 'https://resultados.tse.jus.br/oficial/ele2022/545/dados-simplificados/br/br-c0001-e000545-r.json'
N_SELECTED = (13, 22, 12, 15)
MINUTES    = 5
THRESHOLD  = 23


def tracking_results(url=URL, n_selected=N_SELECTED, minutes=MINUTES, threshold=THRESHOLD):

    """
    Parâmetros
    ----------
    url        (str)          : caminho de interesse na API do TSE
    n_selected (tuple of int) : número dos candidatos
    minutes    (int)          : quantidade de minutos entre cada requisição
    threshold  (int)          : horário de interrupção das requisições

    """
    track = True

    while track:
        # requisição
        results = requests.get(url)
        if (results.status_code != 200):
            break
        
        # dados
        data = json.loads(results.content)
        req_time = data['hg']
        all_candidates = data['cand']
        candidates = [cand for cand in all_candidates if int(cand['n']) in n_selected]

        # construção da tabela
        names, vote_totals, percs = [], [], []
        for cand in candidates:
            nm, vap, pvap = cand['nm'], cand['vap'], cand['pvap']
            names.append(nm)
            vote_totals.append(f'{int(vap):,}')
            percs.append(pvap)
        
        df = pd.DataFrame({'Candidato': names, 'Votação': vote_totals, '%': percs})

        # resultados
        print('------------------------------')
        print(req_time)
        print(df)

        # ciclo
        time.sleep(60 * minutes)

        if (int(req_time[:2]) >= threshold):
            track = False


if __name__ == '__main__':
    tracking_results()

