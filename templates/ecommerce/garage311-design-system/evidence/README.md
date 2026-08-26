# Evidence index

Este índice documenta as evidências usadas por `design-system.json`.

## Capturas e fontes

- `E-live-home-desktop-1440x900-001` — rota inicial pública em `1440 × 900`, DPR 1.
- `E-live-home-mobile-390x844-001` — rota inicial pública em `390 × 844`, DPR 1, com substituição mobile.
- `E-live-product-desktop-1440x900-001` — detalhe público do produto em `1440 × 900`.
- `E-live-product-mobile-390x844-001` — detalhe público do produto em `390 × 844`.
- `E-shot-home-supplied-001` — screenshot longo fornecido pelo usuário, tratado como evidência visual.
- `E-shot-product-supplied-001` — screenshot longo de produto fornecido pelo usuário, tratado como evidência visual.
- `E-source-theme-inline-001` — variáveis inline, declarações de fonte e tema observados na rota pública.
- `E-source-theme-css-001` — regras CSS, media queries, keyframes e dimensões computadas da fonte.
- `E-source-custom-css-001` — CSS customizado e regras responsivas usadas para separar observação de inferência.

## Política de ativos

As capturas raster reais não são distribuídas neste template público porque incluem wordmark, fotografias, banners, textos e outros ativos da loja de referência. O relatório usa espécimes neutros em CSS/SVG e apresenta cartões de evidência como placeholders, evitando quebrar a página ou sugerir autorização de reutilização.

Se houver autorização para uma auditoria privada, os arquivos podem ser adicionados com estes nomes:

```text
live-home-desktop-1440x900.png
live-home-mobile-390x844.png
live-product-desktop-1440x900.png
live-product-mobile-390x844.png
screenshot-home-supplied.png
screenshot-product-supplied.png
```

## Cobertura e limites

- As rotas públicas foram inspecionadas em desktop e mobile estreito.
- A inspeção não prova checkout, autenticação, foco por teclado, autoplay de carrossel ou redução de movimento em runtime.
- `768 × 1024` não foi renderizado; regras de tablet permanecem limitadas às declarações de CSS e às inferências registradas.
- A fonte pode mudar depois do timestamp registrado no manifesto.

Consulte o manifesto para `captured_at`, viewport, método, limitações e IDs de evidência associados a cada token ou regra.
