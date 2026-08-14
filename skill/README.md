<div align="center">
  <img src="assets/icon.svg" width="72" alt="Ícone do Extract Web Design System" />
  <h1>Extract Web Design System</h1>
  <p>
    <strong>Audite. Normalize. Demonstre.</strong><br />
    Reconstrua o sistema por trás de uma interface web — com evidências,<br />
    regras reutilizáveis e uma documentação viva que usa a própria linguagem extraída.
  </p>

  <p>
    <img src="https://img.shields.io/badge/design%20system-FFD400?style=for-the-badge&labelColor=151515" alt="Design system" />
    <img src="https://img.shields.io/badge/evidence--first-F75858?style=for-the-badge&labelColor=151515" alt="Evidence first" />
    <img src="https://img.shields.io/badge/living%20report-FFA43D?style=for-the-badge&labelColor=151515" alt="Living report" />
  </p>

  <p>
    <a href="#como-invocar">Como invocar</a>
    ·
    <a href="#fluxo">Fluxo</a>
    ·
    <a href="#entregaveis">Entregáveis</a>
    ·
    <a href="#quality-gates">Quality gates</a>
  </p>
</div>

---

> Uma skill para estudar a gramática visual e interativa de um produto — não apenas copiar a aparência de uma tela.

<a id="overview"></a>

## ✦ O que é

O <strong>Extract Web Design System</strong> transforma uma referência — site ao vivo, screenshots, gravações, código-fonte ou arquivo de design — em um sistema documentado e rastreável.

O foco é descobrir as regras que fazem a interface funcionar como um conjunto:

| A skill observa | A skill organiza | A skill entrega |
| --- | --- | --- |
| Cores, type, spacing, grid, states e motion | Tokens semânticos, regras responsivas e anatomia de componentes | Manifesto JSON + relatório HTML vivo |
| Rotas, viewports e estados | Evidências, confiança, gaps e exceções | Base para design-to-code e evolução de produto |
| Runtime, DOM/CSS e acessibilidade | Fatos separados de inferências | Handoff reproduzível e honesto |

### O que ela não faz

- não trata um screenshot isolado como prova de comportamento;
- não transforma inferência em fato da fonte;
- não reduz um sistema a uma lista de hex codes;
- não ultrapassa autenticação, CAPTCHA, paywall ou outros controles de acesso;
- não copia desnecessariamente copy, logos, imagens, dados pessoais ou outros ativos protegidos.

<a id="como-invocar"></a>

## ◎ Como invocar

Use a skill pelo nome:

~~~text
Use $extract-web-design-system para extrair este site:
https://exemplo.com

Quero uma análise desktop e mobile com:
- foundations e tokens semânticos;
- componentes, variantes e estados;
- regras responsivas;
- motion e acessibilidade;
- design-system.json;
- report.html com evidências e confiança.
~~~

O metadata da skill está em <code>agents/openai.yaml</code>. Ele define:

- nome de exibição: <strong>Extrair Design System Web</strong>;
- descrição curta para descoberta;
- prompt padrão;
- ícone pequeno e grande;
- disponibilidade para ChatGPT, Codex, API e Atlas;
- permissão para invocação implícita.

### Um prompt bom informa

1. a fonte: URL, screenshots, gravação, repositório ou arquivo de design;
2. o objetivo: documentação, migração, implementação ou comparação visual;
3. o escopo: rotas, temas, viewports, estados e locale;
4. o stack de saída: HTML autocontido ou framework existente;
5. as limitações conhecidas: login, paywall, viewport inacessível ou evidência incompleta.

<a id="entradas"></a>

## ⌁ Entradas suportadas

| Fonte | Método principal | Limite importante |
| --- | --- | --- |
| **URL pública** | Browser inspection, screenshots, computed styles e interação segura | Inspecionar rotas e estados representativos, não só a home |
| **Site autenticado** | Sessão aprovada pelo usuário | Não expor segredos nem executar ações irreversíveis |
| **Screenshots** | Medição visual e comparação entre imagens | Hover, foco, fonte, breakpoint e DOM podem ser apenas inferidos |
| **Screen recording** | Frames, timeline e screenshots | Medir duração considerando frame rate e throttling |
| **Código ou build** | Análise estática + renderização local | Estilos mortos e overrides podem não representar o runtime |
| **Design file ou style guide** | Tokens, componentes e comparação com produção | Separar o especificado do implementado |

Use todas as fontes fornecidas quando possível. Evidências diferentes podem confirmar, contradizer ou limitar a mesma conclusão.

<a id="fluxo"></a>

## ◇ Fluxo de trabalho

~~~mermaid
flowchart TD
  A["Definir escopo e fidelidade"] --> B["Planejar captura"]
  B --> C["Adquirir evidências"]
  C --> D["Normalizar tokens e regras"]
  D --> E["Gerar, verificar e documentar"]
~~~

### 1 · Definir escopo

Registre URLs, artefatos, rotas, temas, locales, estados de login, viewports, objetivo e stack de saída. Se o pedido for aberto, escolha uma amostra representativa:

- home ou landing;
- lista, tabela ou coleção densa;
- detalhe, editor ou formulário;
- navegação aberta/fechada;
- desktop e mobile;
- pelo menos um estado alternativo.

### 2 · Planejar cobertura

Monte uma matriz antes de navegar:

- viewports: mobile estreito, mobile largo, tablet, desktop e wide desktop quando relevantes;
- modos: temas, locale e autenticação;
- estados: default, hover, focus-visible, active, selected, disabled, loading, empty, error, success, open e scrolled;
- regiões: shell, navegação, overlays, formulários, conteúdo, mídia e footer;
- motion: início, intermediário, fim, interrupção e reduced motion.

Não navegue aleatoriamente. Cada célula capturada deve ter um ID de evidência.

### 3 · Adquirir evidências

Colete, quando disponíveis:

- screenshots de página inteira e de componentes com viewport e DPR;
- hierarquia DOM, roles, nomes acessíveis, pseudo-elements e computed styles;
- famílias tipográficas, pesos, eixos variáveis, fallbacks, ícones e tratamento de imagem;
- dimensões, gaps, max-widths, anchors, grids, stacking contexts e overflow;
- transitions, keyframes, easing, delays, stagger, scroll e reduced motion;
- mudanças responsivas entre elementos equivalentes;
- warnings de console/runtime relevantes.

Interações devem ser seguras: hover, foco, abertura/fechamento, tabs, accordions, carousels, validação sem envio e scroll.

### 4 · Normalizar a gramática

Agrupe valores próximos em tokens semânticos sem apagar o valor bruto da evidência. Modele:

- foundations;
- responsive rules;
- motion;
- componentes;
- padrões de página;
- voz e estilo de conteúdo quando houver evidência suficiente.

Prefira nomes de papel, como <code>color.surface.elevated</code>, em vez de nomes acidentais, como <code>gray-50</code>.

### 5 · Reconciliar conflitos

Quando valores divergirem:

1. verifique estado, tema, breakpoint, variante ou exceção;
2. dê preferência à evidência repetida de runtime;
3. mantenha exceções intencionais explícitas;
4. se não houver resolução, mantenha as observações separadas e reduza a confiança.

## ◌ Contrato de evidências

Cada fonte recebe um ID estável, por exemplo <code>E-live-home-desktop-001</code>. Registre:

- tipo e locator da fonte;
- data/hora da captura;
- URL, rota ou nome do arquivo;
- viewport, altura, DPR, zoom, tema, locale e auth state;
- estado e interação usada;
- componente/crop;
- ferramenta ou método;
- notas e limitações.

### Base de cada afirmação

| Base | Significado | Como escrever |
| --- | --- | --- |
| **Observed** | Visível ou inspecionado diretamente | “A superfície usa…” |
| **Computed** | Derivado deterministicamente da evidência | “O contraste calculado é…” |
| **Inferred** | Melhor explicação para observações combinadas | “O breakpoint provável é…” |
| **Recommended** | Sugestão futura, nunca fato da fonte | “Recomenda-se…” |

### Confiança

- **high**: evidência direta repetida, token de origem ou medição correspondente;
- **medium**: padrão consistente em amostra limitada ou inferência forte;
- **low**: estimativa de screenshot, ocorrência única, estado inacessível ou causa ambígua.

<a id="entregaveis"></a>

## ⟡ Entregáveis

A menos que o usuário reduza o escopo, a saída esperada é:

| Arquivo | Papel |
| --- | --- |
| <code>design-system.json</code> | Manifesto machine-readable com tokens, regras, componentes, evidências, confiança, gaps e <code>additional_findings</code> |
| <code>report.html</code> ou projeto de framework | Página viva, responsiva e autocontida que documenta e usa o sistema |
| <code>evidence/</code> | Capturas, referências, probes e limitações, quando for permitido preservá-las |
| Handoff conciso | Cobertura, principais achados, gaps e instruções para reproduzir |

### O manifesto deve cobrir

- papéis de cor e contexto de contraste;
- família, peso, tamanho, line-height, tracking e uso tipográfico;
- escala de spacing e sizing, ou a ausência de uma escala consistente;
- grid, containers, gutters, radii, borders, shadows, icons e imagery;
- breakpoints, reflow, hide/show, order change e substituições;
- trigger, duração, easing, propriedades, stagger e reduced motion;
- anatomia, variantes, tamanhos, estados e restrições de conteúdo;
- evidência e confiança nos claims importantes.

### O relatório vivo deve incluir

1. resumo, escopo, fidelidade, confiança e cobertura;
2. design DNA e princípios visuais;
3. foundations;
4. responsive behavior;
5. motion lab com replay, pause, slow mode e reduced motion;
6. galeria de componentes e estados;
7. composições e padrões de página;
8. acessibilidade e comportamento de conteúdo;
9. evidências, incertezas, exceções e achados adicionais;
10. export de variáveis CSS e tokens de framework quando solicitado.

O relatório deve usar os próprios tokens extraídos. Um shell neutro que apenas exibe swatches não é suficiente.

## ⌘ Quickstart local

A partir desta pasta, valide um manifesto:

~~~bash
python3 scripts/validate_design_system.py \
  path/to/design-system.json
~~~

Gere um relatório autocontido:

~~~bash
python3 scripts/render_design_system_report.py \
  path/to/design-system.json \
  path/to/report.html
~~~

Para servir o resultado localmente:

~~~bash
python3 -m http.server 4173
~~~

Depois, abra <code>http://localhost:4173/path/to/report.html</code>.

Os scripts estão em:

- <code>scripts/validate_design_system.py</code> — valida erros e warnings do manifesto;
- <code>scripts/render_design_system_report.py</code> — gera uma baseline de relatório em um único HTML.

Corrija erros de validação. Warnings são prompts de revisão, não falhas automáticas.

<a id="quality-gates"></a>

## ✓ Quality gates

Não considere a extração concluída sem confirmar:

- dois ou mais viewports materialmente diferentes renderizados e avaliados, ou uma limitação explícita;
- claims interativos apoiados por interação, gravação ou código;
- cores com papéis e contexto de contraste, não apenas hex;
- tipografia com família, peso, tamanho, line-height, tracking e uso;
- spacing e sizing com escala ou ausência documentada;
- motion com trigger, duração, easing, propriedades e reduced motion;
- componentes com anatomia, variantes, estados e comportamento de conteúdo;
- claims principais ligados a evidências e confiança;
- relatório responsivo, navegável por teclado e compatível com reduced motion;
- exemplos de tokens coerentes com seus nomes e valores;
- nenhuma cópia desnecessária de conteúdo protegido.

## ⌂ Stop conditions

Pause, registre o gap e informe o usuário quando:

- autenticação ou permissão estiver faltando;
- CAPTCHA, paywall ou access control impedir o avanço;
- a interação segura não alcançar um estado necessário;
- evidências conflitarem de forma material e não houver rota para resolver;
- a extração expuser dados privados ou copiar conteúdo protegido além da autorização;
- screenshots disponíveis não sustentarem a fidelidade pedida.

Continue com o que é acessível e delimite conclusões. Nunca invente detalhes ausentes.

## ↗ Mapa de arquivos

~~~text
skill/
├── SKILL.md                       # contrato principal da skill
├── README.md                      # guia visual e operacional
├── agents/
│   └── openai.yaml                # metadata e prompt de invocação
├── assets/
│   └── icon.svg                   # ícone da skill
├── references/
│   ├── acquisition-playbook.md    # captura, evidências e stop conditions
│   ├── examples.md                # exemplos e casos-limite
│   ├── extraction-schema.md       # schema do manifesto
│   └── report-spec.md             # arquitetura do relatório vivo
└── scripts/
    ├── validate_design_system.py  # validação do JSON
    └── render_design_system_report.py
~~~

## ≡ Leituras recomendadas

| Arquivo | Quando abrir |
| --- | --- |
| [SKILL.md](SKILL.md) | Antes de executar qualquer extração |
| [acquisition-playbook.md](references/acquisition-playbook.md) | Antes de capturar site, screenshots ou motion |
| [extraction-schema.md](references/extraction-schema.md) | Antes de escrever <code>design-system.json</code> |
| [report-spec.md](references/report-spec.md) | Antes de construir <code>report.html</code> |
| [examples.md](references/examples.md) | Para prompts, screenshots-only, autenticação e conflitos |
| [README da raiz](../README.md) | Para visão geral do repositório e do template Alethe |

---

<div align="center">
  <sub>Observed facts · explicit confidence · reusable grammar · safe evidence</sub>
</div>
