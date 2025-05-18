import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]

    def parse(self, response):
        produtos = response.css('div.poly-card__content')

        for produto in produtos:
            
            
            '''
            A classe dos preços em reais e dos centavos arquiva tanto os preços antigos quanto os novos
            com desconto. Dessa forma, pegamos o primeiro elemento das listas para os preços em reais e em 
            centavos do valor antigo e os segundos elementos da lista  para os valores novos em reais e centavos.
            Já o condicional foi colocado caso no loop o valor não seja encontrado, retonar None e não
            quebrar o código 
            
            Como nas listas de preços queremos que retorne todos os valores e não somente o primeiro valor
            utilizamos o getall() ao invés de somento utilizar o get()
            '''

            precos = produto.css('span.andes-money-amount__fraction::text').getall()
            centavos = produto.css('span.andes-money-amount__cents::text').getall()

            yield {
                'marca': produto.css('span.poly-component__brand::text').get(),
                'nome': produto.css('a.poly-component__title::text').get(),
                'preco_antigo_reais': precos[0] if len(precos) > 0 else None,
                'preco_antigo_centavos': centavos[0] if len(precos) > 0 else None,
                'preco_novo_reais': precos[1] if len(precos) > 1 else None,
                'preco_novo_centavos': centavos[1] if len(centavos) > 1 else None
            }
            
        
