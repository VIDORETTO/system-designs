<div align="center">
  <img src="../../../skill/assets/icon.svg" width="72" alt="Ícone do Garage 311 Commerce Design System" />
  <h1>Garage 311 · Commerce Design System</h1>
  <p>
    <strong>Extração em nível de sistema para uma storefront de peças e acessórios.</strong><br />
    Explore o relatório vivo, consuma o manifesto e confira os limites da evidência.
  </p>

  <p>
    <a href="report.html">Abrir relatório vivo</a>
    ·
    <a href="design-system.json">Ler manifesto</a>
    ·
    <a href="evidence/README.md">Ver índice de evidências</a>
  </p>
</div>

---

> Reconstrução de regras e padrões observáveis — não uma cópia literal da loja nem uma licença para redistribuir seus ativos.

## ✦ O pacote em 30 segundos

Este template documenta a gramática visual e interativa observada no [Garage 311](https://www.garage311.com.br/), com foco em ecommerce de peças para motocicletas.

| Artefato | Para que serve |
| --- | --- |
| `report.html` | Espécime vivo com foundations, componentes, estados, responsividade, motion e export de tokens |
| `design-system.json` | Contrato machine-readable com tokens, regras, componentes, padrões, evidências e gaps |
| `evidence/README.md` | Proveniência, cobertura e política de publicação das capturas |

## ◇ Escopo observado

- shell global, barra de anúncio, busca, conta, carrinho e navegação por categorias;
- home de catálogo com hero, benefícios, rails de produtos, marcas, posts, newsletter e footer;
- detalhe de produto com galeria, preço, pagamento, disponibilidade, descrição, aplicação e relacionados;
- substituições mobile em `390 × 844` e composição desktop em `1440 × 900`;
- motion de hover, overlays, sticky header, escala de imagens e preferências de reduced motion;
- acessibilidade, conteúdo de fitment, suporte flutuante, cookie consent e limitações conhecidas.

## ⌁ Direção visual

O sistema se apoia em azul institucional e azul de ação, navy para navegação, amarelo como acento transacional, superfícies brancas/cinza e uma densidade alta de merchandising. O relatório demonstra essas relações com espécimes neutros: não copia wordmark, fotografias de produtos, banners, textos promocionais ou dados de contato da fonte.

## ◈ Evidências e publicação responsável

As capturas reais usadas durante a extração não estão incluídas neste pacote público. Elas contêm marca, fotografias e conteúdo de terceiros; o índice em [`evidence/README.md`](evidence/README.md) mantém a rastreabilidade sem redistribuir esses ativos.

O manifesto ainda registra as rotas públicas, viewports, métodos e IDs de evidência que sustentam cada conclusão. Para uma auditoria privada, coloque somente arquivos autorizados em `evidence/` usando os nomes documentados no índice.

## ◎ Como usar

Abra `report.html` diretamente no navegador ou sirva a raiz do repositório:

```bash
python3 -m http.server 4173
```

Depois acesse:

```text
http://localhost:4173/templates/ecommerce/garage311-design-system/report.html
```

Valide o manifesto a partir da raiz:

```bash
python3 skill/scripts/validate_design_system.py \
  templates/ecommerce/garage311-design-system/design-system.json
```

## ✓ Reutilização

Use o template como base de raciocínio e composição:

1. importe os tokens semânticos para seu pipeline;
2. adapte grid, densidade, copy e breakpoints ao seu produto;
3. preserve foco visível, estados de compra, tabs, overlays e reduced motion;
4. substitua todos os espécimes por identidade, conteúdo e assets autorizados;
5. revalide contraste, teclado, carrosséis e controles fixos antes de publicar.

## ⌂ Fonte observada

- [Garage 311 · página inicial](https://www.garage311.com.br/)
- [Garage 311 · detalhe do motor de partida](https://www.garage311.com.br/motor-de-partida-arranque-cg150-titan-fan-sport-2004-a-2015-cg125-fan-2009-a-2015-nxr125-nxr150-bros-2006-a-2016)

## ⌘ Limites

Não foram executados checkout, envio de formulário, cálculo de frete, compra, fluxo autenticado, navegação completa por teclado ou captura runtime de reduced motion. O comportamento de tablet e estados não observados permanece marcado como gap ou inferência no manifesto.

---

<div align="center">
  <sub>System-level reconstruction · neutral specimens · traceable evidence</sub>
</div>
