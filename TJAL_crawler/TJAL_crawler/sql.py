import asyncio
from prisma import Prisma

async def create_process(item) -> None:
    db = Prisma()
    await db.connect()
    for value in item.values():
        print("CONNECTED TO DB" + value )
    numero_processo = item['numero_processo']
    classe = item['classeProcesso']
    area = item['area']
    assunto = item['assunto']
    data_distribuicao = item['data_distribuicao']
    juiz = item['juiz']
    valor_total = item['valor_acao']
    grau = item['grau']
    processo = await db.processo_tjal.create(
        data={
            'numero_processo': numero_processo,
            'classe': classe,
            'area': area,
            'assunto': assunto,
            'data_distribuicao': data_distribuicao,
            'juiz': juiz,
            'valor_total': valor_total,
            'grau': grau
        }

    )

    # Create Parte_TJAL records
    for tipo_parte, nomes in item['lista_partes_processo'].items():
        for nome in nomes:
            await db.parte_tjal.create(
                data={
                    'tipo_parte': tipo_parte,
                    'nome': nome.strip(),
                    'processo_id': processo.numero_processo
                }
            )

    # Create Movimentacao_TJAL records
    for data, movimento in item['lista_movimentacoes'].items():
        await db.movimentacao_tjal.create(
            data={
                'data': data,
                'movimento': movimento,
                'processo_id': processo.numero_processo
            }
        )
    await db.disconnect()


async def get_processos(numero_processo:str) -> []:
    db = Prisma()
    await db.connect()
    processo = await db.processo_tjal.find_unique(
        where={
            'numero_processo': numero_processo
        },
        include={
            'parte':True,
            'movimentacao': True
        }
    )
    if not processo:
        print("[get_processos]SEM RETORNO NO DB") ##TODO REMOVER
    else:
        print("retorno: " + processo.numero_processo)
    await db.disconnect()
    return processo

if __name__ == '__main__':
    asyncio.run(create_process())