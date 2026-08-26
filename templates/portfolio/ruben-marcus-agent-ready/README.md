# Ruben Marcus · Agent-ready portfolio

Pacote de extração do design system observado em [rubenmarcus.dev/pt/portfolio](https://www.rubenmarcus.dev/pt/portfolio).

<p>
  <a href="report.html">Abrir relatório vivo</a>
  ·
  <a href="design-system.json">Ler manifesto</a>
  ·
  <a href="evidence/README.md">Ver evidências</a>
</p>

> Este pacote reconstrói regras e padrões observáveis. Não redistribui a fotografia, logos, widgets, fontes ou textos proprietários da referência.

## O pacote

| Arquivo | Função |
| --- | --- |
| `report.html` | espécime autocontido, responsivo e interativo |
| `design-system.json` | tokens, componentes, breakpoints, motion, acessibilidade e proveniência |
| `evidence/README.md` | fontes, estados capturados, limites e política de ativos |

## Assinatura visual

- Canvas preto quase absoluto, texto creme e verde fluorescente para ação, estado e disponibilidade.
- Uncut Sans para display/navegação, Gabarito para leitura e JetBrains Mono para metadados, filtros e ticker.
- Header fixo abaixo de um ticker de 32px; glass + blur de 16px quando a página rola.
- Grid de portfólio 3 → 2 → 1 colunas nos ranges 1080px / 720px, com cards de 16px e borda de 1px.
- Motion em camadas: ticker de 52s, reveal de card de 0,70s, hover default de 0,22s e reduced motion explícito.

## Cobertura

- Runtime desktop: 1440×900, DPR 1.
- Runtime mobile: 390×844, DPR 1.
- Estados seguros: filtro selecionado/reset, hover, foco de teclado, header scrolled, menu mobile aberto/fechado.
- Gravação fornecida: 122,99s, 1862×908, 30fps; usada para ritmo de rolagem e linguagem visual site-wide.
- Confiança geral: medium, porque o tablet foi sustentado por CSS/runtime source e a captura visual mobile do site de origem não pôde ser preservada.

## Como explorar

Abra `report.html` diretamente ou sirva a raiz do repositório:

```bash
python3 -m http.server 4173
```

Depois acesse:

```text
http://localhost:4173/templates/portfolio/ruben-marcus-agent-ready/report.html
```

O relatório demonstra filtro, card hover/focus, menu mobile, input, replay/pause/slow/reduced motion, contraste e export de CSS.

## Validar e regenerar

```bash
python3 skill/scripts/validate_design_system.py \
  templates/portfolio/ruben-marcus-agent-ready/design-system.json

python3 skill/scripts/render_design_system_report.py \
  templates/portfolio/ruben-marcus-agent-ready/design-system.json \
  /tmp/ruben-marcus-agent-ready-baseline.html
```

O `report.html` versionado é uma edição enriquecida que usa o manifesto como fonte; o segundo comando gera a baseline oficial do renderer do repositório.

## Reuso responsável

Use os tokens e a gramática como ponto de partida, não como cópia de marca. Substitua espécimes por identidade, conteúdo e ativos próprios; confirme licenças de fontes, imagens, ícones e marcas antes de publicar uma implementação comercial.
