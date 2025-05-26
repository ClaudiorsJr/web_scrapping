import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    max_pages = 10

    def parse(self, response):
        
        produtos = response.css('div.poly-card__content')

        current_page = response.meta.get('page', 1)

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
                'preco_antigo_centavos': centavos[0] if len(centavos) > 0 else None,
                'preco_novo_reais': precos[1] if len(precos) > 1 else None,
                'preco_novo_centavos': centavos[1] if len(centavos) > 1 else None,
                'reviews_nota': produto.css('span.poly-reviews__rating::text').get(),
                'quantidade_reviews': produto.css('span.poly-reviews__total::text').get()
            }

        '''
        Para seguir para as próximas páginas e continuar o scrapping, utilizamos o elemento do botão de próxima
        página e ao final utilizamos "a::attr(href)" quedireciona para o link da próxima página
        ''' 
         # Paginação
        if current_page < self.max_pages:
            next_page = response.css('li.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                yield scrapy.Request(
                    url=next_page,
                    callback=self.parse,
                    meta={'page': current_page + 1},
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
                )
