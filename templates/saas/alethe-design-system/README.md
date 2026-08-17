<div align="center">
  <img src="../../../skill/assets/icon.svg" width="72" alt="Ícone do Alethe Agents Design System" />
  <h1>Alethe Agents · Design System Extraction</h1>
  <p>
    <strong>Um sistema vivo para estudar, reutilizar e evoluir uma linguagem de interface.</strong><br />
    Explore o espécime visual, leia o contrato de tokens e rastreie<br />
    cada decisão até sua evidência — com limites claros.
  </p>

  <p>
    <img src="https://img.shields.io/badge/living%20report-FFD400?style=for-the-badge&labelColor=151515" alt="Living report" />
    <img src="https://img.shields.io/badge/evidence%20indexed-F75858?style=for-the-badge&labelColor=151515" alt="Evidências indexadas" />
    <img src="https://img.shields.io/badge/no%20runtime%20deps-FFA43D?style=for-the-badge&labelColor=151515" alt="Sem dependências externas de runtime" />
  </p>

  <p>
    <a href="report.html">Abrir relatório vivo</a>
    ·
    <a href="design-system.json">Ler manifesto</a>
    ·
    <a href="evidence/README.md">Ver evidências</a>
  </p>

  <p>
    <a href="#overview">Visão rápida</a>
    ·
    <a href="#report">Relatório</a>
    ·
    <a href="#tokens">Tokens</a>
    ·
    <a href="#evidence">Evidências</a>
    ·
    <a href="#reuse">Reutilização</a>
  </p>
</div>

---

> Este pacote reconstrói regras e padrões observáveis. Ele não é uma cópia literal da landing page nem uma licença para redistribuir seus ativos.

<a id="overview"></a>

## ✦ O pacote em 30 segundos

O Alethe Agents Design System é um artefato de extração em nível de sistema, baseado na inspeção pública da landing page do Alethe Agents.

| O que você encontra | Para que serve |
| --- | --- |
| Página viva e interativa | Ver foundations, componentes, estados, temas, motion e composição em ação |
| Manifesto JSON | Consumir tokens, regras e evidências em automação |
| Evidence index | Entender fontes, probes, cobertura e limitações |
| README do pacote | Reproduzir a leitura e adaptar o sistema com responsabilidade |

### Escopo observado

- landing page pública;
- shell e navegação global;
- hero e composição principal;
- canvas de orquestração;
- feature grid;
- seletor de temas;
- download pitch;
- footer;
- captura principal em desktop, 1363 × 936, DPR 1;
- tema observado: dark-lemon;
- confiança geral: medium.

## ⌁ Como ler o pacote

~~~mermaid
flowchart LR
  A["Fonte pública"] --> B["Manifesto"]
  B --> C["Relatório vivo"]
  C --> D["Evidence index"]
  D --> E["Adaptação própria"]
~~~

Leia os arquivos nesta ordem:

1. **report.html** para entender o sistema visualmente;
2. **design-system.json** para localizar tokens e regras;
3. **evidence/README.md** para verificar a origem das conclusões;
4. **este README** para direção visual, acessibilidade, limites e reuso.

<a id="report"></a>

## ◇ O relatório vivo

Abra <a href="report.html"><code>report.html</code></a> para explorar uma documentação que demonstra o próprio sistema.

Ele reúne:

- resumo executivo, escopo, fidelidade e confiança;
- design DNA e princípios visuais;
- color, typography, spacing, sizing, grid, radii, borders, shadows e icons;
- temas e responsive specimen;
- motion lab com replay, pause, slow mode e reduced motion;
- componentes, variantes e estados;
- composições de página;
- acessibilidade e comportamento de conteúdo;
- evidências, gaps e exceções;
- exportação de variáveis CSS.

### Como abrir

#### Opção rápida

Abra <code>report.html</code> diretamente no navegador. Ele é autocontido e não depende de build, framework ou pacote externo.

#### Opção recomendada

A partir da raiz do repositório, sirva os arquivos localmente:

~~~bash
python3 -m http.server 4173
~~~

Depois, acesse:

~~~text
http://localhost:4173/templates/saas/alethe-design-system/report.html
~~~

Servir localmente é preferível quando você quiser testar clipboard, links, keyboard navigation e interações sem restrições do navegador.

<a id="tokens"></a>

## ⟡ O manifesto de tokens

Abra <a href="design-system.json"><code>design-system.json</code></a> para consumir o contrato machine-readable do pacote.

Ele pode alimentar:

- variáveis CSS;
- temas;
- Tailwind ou Style Dictionary;
- documentação;
- componentes;
- testes visuais;
- pipelines de design-to-code;
- comparações entre versões.

### Snapshot da assinatura visual

| Token | Valor observado | Papel |
| --- | --- | --- |
| <code>--frame</code> | <code>#050505</code> | Canvas externo e trilhos |
| <code>--bg</code> | <code>#121317</code> | Superfície principal |
| <code>--ink</code> | <code>#fafafa</code> | Texto de maior prioridade |
| <code>--ink-dim</code> | <code>#9a9a9e</code> | Texto de apoio |
| <code>--accent</code> | <code>#ffff50</code> | Seleção, ação e sinal principal |
| <code>--line</code> | <code>rgba(255,255,255,.06)</code> | Hairlines e separação |
| <code>--font-display</code> | <code>Anton</code> + fallback | Títulos e presença editorial |
| <code>--font-sans</code> | <code>Geist</code> + fallback | Corpo e interface |
| <code>--font-mono</code> | <code>Geist Mono</code> + fallback | Status, labels e dados |
| <code>--ease</code> | <code>cubic-bezier(.16,1,.3,1)</code> | Easing principal |

Os nomes das famílias permanecem documentados, mas arquivos proprietários não foram copiados. Use fallbacks locais quando as fontes não estiverem disponíveis.

## ◌ Direção visual

A assinatura do sistema depende mais da relação entre princípios do que de uma cor isolada:

| Princípio | Expressão visual | Regra de uso |
| --- | --- | --- |
| **Technical frame** | Frame central de aproximadamente 1280px, trilhos, hairlines e marcas de registro | Faça o produto parecer um instrumento operacional |
| **Operational contrast** | Superfícies quase pretas, branco forte, metadados discretos e um acento vívido | Reserve o contraste máximo para hierarquia, ação e estado |
| **Proof through UI** | Terminais, árvores, grids, dots, panes e canvas | Mostre capacidade através de interface observável |
| **Theme as accent** | A estrutura permanece estável enquanto o acento muda | Troque o sinal cromático sem desmontar a arquitetura |
| **Dense details, quiet rhythm** | Tipografia grande e microcopy mono equilibradas por espaço negativo | Use densidade para informar, não para preencher |

### Sensação desejada

O resultado deve parecer técnico, preciso, controlável e levemente experimental. Elementos pequenos precisam comunicar status, contexto, origem ou prova.

## ↗ Motion contract

O relatório inclui um laboratório para experimentar o contrato temporal extraído:

| Faixa | Uso sugerido |
| --- | --- |
| <code>120–200ms</code> | Hover, chip, botão e microinterações |
| <code>350–600ms</code> | Tema, reveal, entrada de card e mudança de estado |
| <code>700–1100ms</code> | Desenho de linha, fluxo, blink e orquestração |
| <code>0.001ms</code> | Redução de movimento e acessibilidade |

O easing principal favorece entradas e deslocamentos com desaceleração expressiva, sem elasticidade decorativa excessiva.

<a id="evidence"></a>

## ◈ Evidências e limitações

O índice completo está em <a href="evidence/README.md"><code>evidence/README.md</code></a>.

### Cobertura registrada

- <code>E-live-home-desktop-001</code> — página inicial pública em 1363 × 936, DPR 1;
- <code>E-live-fullpage-desktop-002</code> — captura de página inteira, aproximadamente 5034px;
- <code>E-dom-css-desktop-003</code> — DOM, acessibilidade, computed styles, fontes, media rules, keyframes, variáveis e medidas;
- <code>E-live-theme-004</code> — 11 controles de tema ativados e verificados;
- <code>E-live-usecase-005</code> — use case “Caçar bug” selecionado e mudança de conteúdo observada;
- <code>E-live-hover-006</code> — hover no primeiro feature cell;
- <code>E-live-keyboard-007</code> — avanço por Tab e foco visível;
- <code>E-skill-contract-008</code> — contrato da skill usado como critério de evidência e qualidade.

### Limitações importantes

- a inspeção runtime teve acesso direto a um viewport desktop; não houve captura pareada em viewport estreito;
- o comportamento mobile foi representado a partir das media/container queries e marcado como observado na fonte ou inferido no manifesto;
- arte original, wordmark, screenshot de produto, avatar e logos de terceiros foram omitidos;
- espécimes neutros em CSS/SVG demonstram as regras sem redistribuir conteúdo protegido.

Não leia um breakpoint ou uma animação como fato de runtime se a evidência disponível for apenas uma declaração de CSS ou uma imagem estática.

## ✓ Acessibilidade incluída

O relatório demonstra e documenta:

- landmarks, headings e navegação interna;
- estados selecionados com <code>aria-pressed</code>;
- foco visível com outline de 2px e offset de 2px;
- tabs com <code>aria-controls</code>, <code>tabpanel</code> e roving <code>tabindex</code>;
- estado <code>disabled</code> real;
- live regions para alterações de use case e motion;
- ramo de <code>prefers-reduced-motion</code>;
- fallback quando JavaScript ou observer não estiverem disponíveis;
- quebra segura de textos longos e prevenção de sobreposição.

<a id="reuse"></a>

## ⌘ Como transformar em produto real

Use este pacote como uma base de raciocínio e composição:

1. importe o manifesto para o pipeline de tokens;
2. gere variáveis CSS, Tailwind ou Style Dictionary;
3. crie componentes base para header, chip, agent card, status dot, window chrome, painel, tabela e motion wrapper;
4. modele variantes semânticas para estados operacionais e temas;
5. preserve labels, foco visível, <code>aria-pressed</code> e reduced motion;
6. monte dashboards, integrações, automações, billing e configurações com a mesma gramática;
7. substitua espécimes por identidade, conteúdo e assets próprios;
8. adicione testes visuais em desktop e viewports estreitos.

### Onde funciona bem

- dashboards de agentes e orquestração;
- ferramentas para desenvolvedores;
- produtos de IA com múltiplos modelos;
- backoffice operacional;
- SaaS B2B, infraestrutura, automação, segurança e dados.

### Onde adaptar com cuidado

Produtos infantis, marcas de bem-estar, experiências muito acolhedoras, e-commerces extremamente promocionais e interfaces em que calor humano ou acessibilidade cromática precisam ser o sinal dominante exigem uma adaptação maior de acento, contraste, display type e densidade.

## ⌘ Validação do pacote

O pacote foi validado com:

- manifesto <code>design-system.json</code>: 0 erros e 0 warnings;
- JavaScript inline compilável;
- CSS com chaves balanceadas;
- IDs HTML únicos;
- links internos com destinos existentes;
- 36 botões com nome acessível;
- fallbacks de reveal, clipboard, overflow e layout final;
- isolamento do elemento decorativo do footer.

Para reproduzir a validação a partir da raiz do repositório:

~~~bash
python3 skill/scripts/validate_design_system.py \
  templates/saas/alethe-design-system/design-system.json
~~~

Para gerar uma nova baseline:

~~~bash
python3 skill/scripts/render_design_system_report.py \
  templates/saas/alethe-design-system/design-system.json \
  /tmp/design-system-report.html
~~~

## ⌂ Direitos e publicação

Este pacote é uma reconstrução de system design baseada em observação pública. Antes de publicar uma implementação comercial:

- substitua espécimes por identidade própria;
- confirme direitos de fontes, imagens, ícones, marcas e conteúdos;
- não redistribua ativos omitidos da referência;
- mantenha a proveniência e as limitações visíveis;
- descreva diferenças materiais em vez de prometer pixel perfection sem comparação equivalente.

## ▣ Estrutura do pacote

~~~text
alethe-design-system/
├── README.md                 # este guia
├── report.html               # relatório vivo e autocontido
├── design-system.json        # tokens, regras e evidências
└── evidence/
    └── README.md             # índice de capturas e limitações
~~~

## ≡ Leituras relacionadas

| Arquivo | Para aprofundar |
| --- | --- |
| [Templates](../../README.md) | Catálogo e contrato dos pacotes |
| [README da skill](../../../skill/README.md) | Como executar uma nova extração |
| [SKILL.md](../../../skill/SKILL.md) | Contrato operacional completo |
| [Extraction schema](../../../skill/references/extraction-schema.md) | Estrutura do manifesto |
| [Report spec](../../../skill/references/report-spec.md) | Arquitetura do relatório vivo |
| [Acquisition playbook](../../../skill/references/acquisition-playbook.md) | Captura e evidências |
| [Fonte observada](https://alethe-agents.kc1t.com/) | Página pública usada como referência |

---

<div align="center">
  <sub>System-level reconstruction · neutral specimens · traceable evidence</sub>
</div>

