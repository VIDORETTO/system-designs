<div align="center">
  <img src="skill/assets/icon.svg" width="72" alt="Ícone do Web Design System Extraction" />
  <h1>Web Design System Extraction</h1>
  <p>
    <strong>Do site à linguagem de interface.</strong><br />
    Extraia padrões visuais e comportamentais, transforme evidências em tokens<br />
    e entregue uma documentação viva que demonstra o próprio sistema.
  </p>

  <p>
    <img src="https://img.shields.io/badge/AI%20skill-design%20system-FFD400?style=for-the-badge&labelColor=151515" alt="AI skill para design systems" />
    <img src="https://img.shields.io/badge/evidence-first-F75858?style=for-the-badge&labelColor=151515" alt="Fluxo orientado por evidências" />
    <img src="https://img.shields.io/badge/HTML%20%2B%20JSON-FFA43D?style=for-the-badge&labelColor=151515" alt="Saída em HTML e JSON" />
  </p>

  <p>
    <a href="#visao-rapida">Visão rápida</a>
    ·
    <a href="#como-usar">Como usar</a>
    ·
    <a href="#o-que-e-gerado">Saídas</a>
    ·
    <a href="#criterios-de-qualidade">Qualidade</a>
  </p>
</div>

---

> Uma skill para estudar o sistema por trás de uma interface — não apenas reproduzir a aparência de uma tela.

<a id="visao-rapida"></a>

## ✦ Visão rápida

Este projeto reconstrói a gramática visual e interativa de um produto a partir de uma URL, screenshots, gravações, código-fonte ou arquivos de design. O resultado combina documentação, automação e uma página viva para explorar o sistema.

| Entrada | Processo | Resultado |
| --- | --- | --- |
| URL, screenshots, gravação ou código | Evidências → padrões → tokens → regras | Manifesto legível por máquina + relatório visual |
| Estados, viewports e interações | Observado, computado, inferido e recomendado | Decisões rastreáveis e limites explícitos |
| Componentes e páginas representativas | Auditoria visual, responsiva e de acessibilidade | Base reutilizável para design-to-code |

### Em uma frase

**Observe com contexto. Normalize sem apagar exceções. Demonstre usando o próprio sistema.**

## ◇ O que a skill resolve

A extração não termina em uma coleção de cores. Ela procura as regras que fazem uma interface parecer coerente:

- fundamentos: cores semânticas, tipografia, espaçamento, grid, sizing, bordas, raios, sombras, ícones e imagens;
- comportamento: breakpoints, reflow, substituição mobile, densidade, overflow e composição;
- interação: hover, foco, seleção, loading, erro, sucesso, abertura, fechamento e estados desabilitados;
- motion: gatilho, duração, easing, propriedades, stagger, interrupção e redução de movimento;
- componentes: anatomia, variantes, estados, limites de conteúdo e comportamento acessível;
- padrões de página: shell, navegação, seções, hierarquia e templates recorrentes;
- evidências: origem, contexto, captura, confiança, limitações e gaps.

## ⌁ O fluxo

~~~mermaid
flowchart LR
  A["Fonte visual"] --> B["Plano de captura"]
  B --> C["Evidências"]
  C --> D["Tokens e regras"]
  D --> E["Relatório vivo"]
~~~

Cada conclusão importante deve conseguir responder a três perguntas:

1. **De onde veio?** URL, screenshot, DOM/CSS, gravação ou arquivo de origem.
2. **O que é fato?** Observado ou computado diretamente.
3. **O que é leitura?** Inferido ou recomendado, com confiança declarada.

<a id="como-usar"></a>

## ◎ Como usar

A skill pode ser invocada no ChatGPT, Codex ou outro ambiente compatível com skills:

~~~text
Use $extract-web-design-system para extrair o design system deste site:
https://exemplo.com

Quero:
- cobertura desktop e mobile;
- tokens de cor e tipografia;
- componentes e estados;
- regras responsivas;
- motion e acessibilidade;
- design-system.json e report.html.
~~~

Também é possível trabalhar com:

| Rota | Quando usar | Principal cuidado |
| --- | --- | --- |
| **Site ao vivo** | Auditoria completa de uma experiência pública | Capturar rotas e estados representativos, não só a home |
| **Sessão autenticada** | Fluxos que dependem de login | Usar apenas uma sessão aprovada e evitar ações irreversíveis |
| **Screenshots** | Referência visual sem acesso ao produto | Marcar fontes, breakpoints e interações como inferidos quando necessário |
| **Screen recording** | Análise de motion e transições | Medir o intervalo e registrar trigger, entrada e saída |
| **Código ou build** | Reutilização em uma base existente | Confirmar runtime: estilos mortos e overrides podem distorcer a leitura |
| **Arquivo de design ou style guide** | Comparar especificação e implementação | Separar o que foi especificado do que realmente foi implementado |

Quando o escopo não for definido, a cobertura mínima recomendada é:

- mobile estreito: <code>390 × 844</code>;
- tablet: <code>768 × 1024</code>, quando houver mudança material;
- desktop: <code>1440 × 900</code>;
- uma página de entrada, uma página densa, uma página de detalhe/formulário e pelo menos um overlay ou estado alternativo.

<a id="o-que-e-gerado"></a>

## ⟡ O que é gerado

### <code>design-system.json</code>

O contrato normalizado para automação. Reúne:

- tokens semânticos e aliases;
- regras responsivas;
- motion e preferências de redução;
- anatomia e estados de componentes;
- padrões de composição;
- evidências, confiança, gaps e exceções;
- <code>additional_findings</code> para descobertas fora da taxonomia principal.

### <code>report.html</code>

Uma página responsiva, autocontida e interativa que documenta e utiliza os tokens extraídos. A estrutura padrão inclui:

1. resumo executivo, escopo e cobertura;
2. princípios visuais e design DNA;
3. foundations;
4. regras responsivas;
5. laboratório de motion;
6. galeria de componentes e estados;
7. padrões de página;
8. acessibilidade e comportamento de conteúdo;
9. evidências, incertezas e exceções;
10. variáveis CSS e exports copiáveis.

### <code>evidence/</code>

Índice das capturas, probes e limitações usadas para sustentar o manifesto. Quando a fonte for apenas código, a proveniência pode permanecer dentro do próprio <code>design-system.json</code>.

## ▣ Estrutura do repositório

~~~text
system-designs/
├── README.md
├── skill/
│   ├── SKILL.md                       # instruções principais da skill
│   ├── agents/openai.yaml             # nome, descrição e prompt padrão
│   ├── assets/icon.svg                # ícone da skill
│   ├── references/
│   │   ├── acquisition-playbook.md    # cobertura e protocolo de evidências
│   │   ├── examples.md                # exemplos e casos-limite
│   │   ├── extraction-schema.md       # contrato do manifesto JSON
│   │   └── report-spec.md             # especificação do relatório vivo
│   └── scripts/
│       ├── validate_design_system.py  # validação do manifesto
│       └── render_design_system_report.py
└── templates/
    ├── saas/
    │   ├── README.md
    │   └── alethe-design-system/
    │       ├── README.md
    │       ├── design-system.json
    │       ├── report.html
    │       └── evidence/README.md
    ├── ecommerce/README.md
    ├── finance/README.md
    ├── healthcare/README.md
    ├── education/README.md
    ├── media/README.md
    └── portfolio/README.md
~~~

## ↗ Documentação de apoio

| Arquivo | Para aprofundar |
| --- | --- |
| [SKILL.md](skill/SKILL.md) | Contrato operacional completo da skill |
| [acquisition-playbook.md](skill/references/acquisition-playbook.md) | Plano de captura, evidências e limites |
| [extraction-schema.md](skill/references/extraction-schema.md) | Estrutura do manifesto <code>design-system.json</code> |
| [report-spec.md](skill/references/report-spec.md) | Arquitetura e critérios do relatório vivo |
| [Template Alethe](templates/saas/alethe-design-system/README.md) | Exemplo completo de pacote gerado |

## ⌘ Quickstart local

Valide um manifesto existente:

~~~bash
python3 skill/scripts/validate_design_system.py \
  templates/saas/alethe-design-system/design-system.json
~~~

Gere um relatório autocontido a partir dele:

~~~bash
python3 skill/scripts/render_design_system_report.py \
  templates/saas/alethe-design-system/design-system.json \
  /tmp/design-system-report.html
~~~

Depois, abra <code>/tmp/design-system-report.html</code> no navegador. O template incluído em <code>templates/saas/alethe-design-system/</code> funciona como referência completa de manifesto, relatório e índice de evidências.

## ◌ Princípios de leitura

O sistema separa a força de cada afirmação para que documentação e hipótese não se misturem:

| Base | Significado | Exemplo |
| --- | --- | --- |
| **Observed** | Visível ou inspecionado diretamente | Uma cor aparece em cinco botões |
| **Computed** | Derivado deterministicamente da evidência | Contraste ou duração calculados |
| **Inferred** | Melhor explicação para múltiplas observações | Um breakpoint provável |
| **Recommended** | Sugestão de evolução, nunca fato da fonte | Uma alternativa de foco mais clara |

Cada item também recebe confiança:

- **high**: evidência direta, repetida ou token de origem;
- **medium**: padrão consistente em uma amostra limitada;
- **low**: estimativa visual, ocorrência única ou estado inacessível.

<a id="criterios-de-qualidade"></a>

## ✓ Critérios de qualidade

Uma extração só está pronta quando:

- pelo menos dois viewports materialmente diferentes foram renderizados e avaliados, ou a limitação está explícita;
- claims de interação têm evidência de interação, gravação ou código;
- cores têm papéis semânticos e contexto de contraste;
- tipografia registra família, peso, tamanho, line-height, tracking e uso;
- espaçamento e sizing revelam uma escala ou documentam a ausência dela;
- motion registra trigger, duração, easing, propriedades e reduced motion;
- componentes incluem anatomia, variantes, estados e comportamento de conteúdo;
- as principais conclusões apontam para evidências e confiança;
- o relatório usa os tokens extraídos e passa por revisão responsiva, de teclado e de reduced motion.

## ◈ Regra de ouro do relatório

O relatório não deve ser um shell neutro que apenas exibe swatches.

Ele precisa **parecer e se comportar como uma amostra do sistema extraído**, usando suas próprias variáveis de cor, tipografia, espaçamento, formas, grid e motion. Quando um valor for apenas um fallback de documentação, ele deve ser identificado como fallback — e não entrar silenciosamente no manifesto.

## ⌂ Privacidade, direitos e escopo

- Não ultrapasse autenticação, CAPTCHA, paywall ou outros controles de acesso.
- Não copie desnecessariamente logos, wordmarks, fotos, textos proprietários ou dados pessoais.
- Prefira espécimes neutros em CSS/SVG quando a referência contiver conteúdo protegido.
- Registre limitações e estados inacessíveis em vez de inventar comportamentos.
- Separe com clareza o que veio da fonte do que foi recomendado para uma implementação futura.

---

<div align="center">
  <sub>Evidence first · tokens with context · reports that demonstrate the system</sub>
</div>


## ✦ Experience Layer: quando o design é mais do que tokens

A skill agora registra a camada que costuma desaparecer em inventários genéricos:

- identidade, sensory words, anti-generic constraints e focal moment;
- elementos de assinatura: textura, grain, silhouette, divider, cursor response e relações de camada;
- mídia como composição: vídeo de background, poster, crop, scrim, text-safe zone, playback, performance e fallback;
- efeitos com driver/job/fallback: scroll reveal, pointer glow, blur, blend, gradient, canvas e shader;
- motion com propósito, não apenas duração: feedback, continuidade, hierarquia, atmosfera, navegação, estado e delight.

Para investigar essa camada, use:

    python3 skill/scripts/probe_media_inventory.py SOURCE --output inventory.json

Em uma sessão de navegador autorizada, use skill/scripts/runtime_media_probe.js. Para um vídeo autorizado, use skill/scripts/extract_video_frames.py VIDEO OUTPUT_DIR --count 6. A documentação não baixa, reproduz ou embute mídia protegida automaticamente.

O novo fixture em templates/media/experience-layer/ mostra o contrato v2 com background video, poster local neutro, relatório vivo, effects, motion lab, reduced-motion e provenance.



## ✦ Production hardening

Depois da primeira implementação, a skill ganhou um gate executável de browser:

- Playwright pinado para capturar rotas, viewports desktop/mobile e reduced-motion;
- manifest de captura com screenshots, page errors, request failures e runtime probe;
- validação de cobertura normal/reduced-motion;
- comparação visual por pixels com Pillow quando há baseline revisado;
- GitHub Actions para rodar o contrato, renderer, fixtures, browser smoke e visual gate;
- runbook de promoção de baselines e limites de autorização.

Comandos principais:

    npm install
    npx playwright install chromium
    npm run capture:browser
    npm run validate:browser
    npm run visual:regression

O fixture `experience-layer` já possui baseline revisado para desktop/mobile e normal/reduced-motion; a CI bloqueia mudanças acima do limite de pixels. Novos targets entram como `baseline-pending` somente durante o bootstrap autorizado.

