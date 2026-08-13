# Alethe Agents · Design System Extraction

> Um pacote autocontido para estudar, reutilizar e evoluir a linguagem visual e interativa do Alethe Agents.

[Abrir o relatório vivo](report.html) · [Ler o manifesto](design-system.json) · [Consultar as evidências](evidence/README.md)

| Entrega | Status |
| --- | --- |
| Página viva do design system | pronta |
| Tokens e regras normalizados | prontos |
| Evidências e limitações | documentadas |
| Dependências de runtime | nenhuma |
| Captura principal | desktop, 1363 × 936, DPR 1 |

## Visão geral

Este pacote transforma a inspeção pública do Alethe Agents em um artefato reutilizável: uma página que demonstra o próprio sistema visual, um manifesto legível por máquina e um índice de evidências que separa o que foi observado do que foi inferido.

O resultado não é uma cópia literal da landing page. A estrutura preserva a gramática visual e de interação — frame técnico, contraste operacional, tipografia display, estados de agentes, temas, motion e composição — usando espécimes neutros em CSS/SVG quando a referência continha arte, marca ou conteúdo protegido.

## Estrutura do pacote

```text
alethe-design-system/
├── README.md                 # Guia de uso, linguagem visual e recomendações
├── report.html                # Página viva e autocontida do design system
├── design-system.json         # Manifesto normalizado de tokens e evidências
└── evidence/
    └── README.md              # Índice das capturas, probes e limitações
```

### Papel de cada arquivo

- `report.html` é a referência visual principal. Ele contém foundations, temas, responsive specimen, motion lab, componentes, composições, acessibilidade, evidências e exportação de tokens.
- `design-system.json` é o contrato para automação. Pode alimentar documentação, tokens CSS, temas, componentes, testes visuais ou um pipeline de design-to-code.
- `evidence/README.md` registra a origem das conclusões, os experimentos realizados e os limites de cobertura da extração.

## Como abrir

### Opção rápida

Abra `report.html` diretamente no navegador. A página é autocontida e não depende de build, framework ou pacote externo.

### Opção recomendada

Servir a pasta localmente evita restrições de clipboard em alguns navegadores:

```bash
python3 -m http.server 4173
```

Depois acesse:

```text
http://localhost:4173/alethe-design-system/report.html
```

No Windows, `py -m http.server 4173` produz o mesmo resultado quando o Python está instalado.

## Direção visual

O sistema foi organizado em cinco princípios. Eles são mais importantes do que qualquer cor isolada:

| Princípio | Expressão visual | Regra de uso |
| --- | --- | --- |
| **Technical frame** | Frame central de 1280px, trilhos laterais hachurados, hairlines e marcas de registro | Faça o produto parecer um instrumento operacional, não um card genérico |
| **Operational contrast** | Superfícies quase pretas, branco forte, metadados discretos e um acento vívido | Reserve o contraste máximo para hierarquia, ação e estado |
| **Proof through UI** | Terminais, árvores, grids, dots, panes e canvas de orquestração | Mostre a capacidade do produto por meio de interface observável |
| **Theme as accent** | A estrutura permanece estável enquanto o acento muda | Troque o sinal cromático sem desmontar a arquitetura visual |
| **Dense details, quiet rhythm** | Tipografia grande e espaço negativo equilibrados por microcopy monospace | Use densidade para informar, não para preencher cada área vazia |

### Sensação desejada

O resultado deve parecer técnico, preciso, controlável e levemente experimental. A interface pode ser densa, mas precisa continuar legível: cada elemento pequeno deve comunicar status, contexto, origem ou prova.

## Tokens essenciais

O manifesto contém a versão completa. Esta tabela resume os tokens que formam a assinatura visual:

| Token | Valor observado | Função |
| --- | --- | --- |
| `--frame` | `#050505` | Canvas externo e trilhos |
| `--bg` | `#121317` | Superfície principal |
| `--ink` | `#fafafa` | Texto e títulos de maior prioridade |
| `--ink-dim` | `#9a9a9e` | Texto de apoio |
| `--accent` | `#ffff50` | Seleção, ação e sinal principal |
| `--line` | `rgba(255,255,255,.06)` | Hairlines e separação sutil |
| `--font-display` | `Anton` com fallback | Teses, títulos e presença editorial |
| `--font-sans` | `Geist` com fallback | Corpo, interface e leitura |
| `--font-mono` | `Geist Mono` com fallback | Status, labels, evidências e dados |
| `--ease` | `cubic-bezier(.16,1,.3,1)` | Easing principal |

Os nomes das famílias observadas permanecem no sistema, mas os arquivos proprietários não foram copiados. O navegador usa fallbacks locais quando elas não estão disponíveis.

## Regras de composição

- Mantenha um frame centralizado de aproximadamente `1280px` em telas largas.
- Use bordas finas e espaçamento consistente para criar a malha; evite sombras genéricas em excesso.
- Use a fonte display para tese visual e a monospace para informação operacional.
- Trate o acento como um sinal escasso: seleção, foco, CTA, estado relevante e pontos de atividade.
- Nunca comunique estado apenas pela cor. Combine dot, texto, label ou mudança de forma.
- Em telas estreitas, empilhe colunas, permita quebra de textos e preserve o fluxo natural do documento.
- Elementos decorativos podem ser intensos, mas nunca devem competir com texto, foco ou informação de estado.

## Motion contract

O laboratório de movimento do relatório permite testar o contrato temporal extraído:

| Faixa | Uso sugerido |
| --- | --- |
| `120–200ms` | Hover, chip, botão e microinterações |
| `350–600ms` | Tema, reveal, entrada de card e mudança de estado |
| `700–1100ms` | Desenho de linha, fluxo, blink e orquestração |
| `0.001ms` | Redução de movimento e acessibilidade |

O easing principal deve ser preservado para que entradas e deslocamentos tenham uma desaceleração expressiva, sem parecerem elásticos ou decorativos demais.

## Onde este design system funciona bem

### 1. Dashboards de agentes e orquestração

Ideal para mostrar agentes em execução, filas, dependências, logs, tarefas, consumo de contexto e estados como `running`, `waiting`, `done` e `stopped`.

### 2. Ferramentas para desenvolvedores

Combina com terminal web, observabilidade, debugging, pipelines, automações, ambientes de execução e produtos que precisam transmitir controle técnico.

### 3. Produtos de IA com múltiplos modelos

O sistema de temas, dots, cards e panes funciona bem para comparar modelos, visualizar roteamento, acompanhar custo e explicar decisões de um orquestrador.

### 4. Backoffice operacional

Pode servir como base para gestão de integrações, permissões, billing, configurações, filas de atendimento, operações internas e ferramentas administrativas de alta densidade.

### 5. Landing pages de produtos técnicos

A composição baseada em tese visual + prova de interface é adequada para SaaS B2B, infraestrutura, automação, segurança, dados e developer tools.

### Onde usar com cuidado

O sistema não é a melhor escolha sem adaptação para produtos infantis, marcas de bem-estar, experiências muito acolhedoras, e-commerces extremamente promocionais ou interfaces em que calor humano e acessibilidade cromática precisam ser o sinal dominante. Nesses casos, preserve a disciplina estrutural, mas reavalie acento, contraste, display type e densidade.

## Como transformar em produto real

Uma evolução prática pode seguir esta ordem:

1. Importar `design-system.json` para um pipeline de tokens e gerar variáveis CSS, Tailwind ou Style Dictionary.
2. Criar componentes base para header, chip, card de agente, status dot, window chrome, painel, tabela e motion wrapper.
3. Definir variantes semânticas para estados operacionais e temas, mantendo `aria-pressed`, labels e foco visível.
4. Montar telas de dashboard, gestão de agentes, automações, integrações, billing e configurações usando a mesma gramática.
5. Adicionar testes visuais em desktop e em viewports estreitos, especialmente para grids, exportação, rodapé e conteúdo longo.
6. Substituir os espécimes neutros por ativos próprios somente depois de validar licenças, acessibilidade e consistência de marca.

## Acessibilidade incluída

O relatório demonstra e documenta:

- landmarks, headings e navegação interna;
- estados selecionados com `aria-pressed`;
- foco visível com outline de 2px e offset de 2px;
- controles de tabs com `aria-controls`, `tabpanel` e roving `tabindex`;
- estado `disabled` real no botão de demonstração;
- live regions para mudanças de use case e motion;
- ramo de `prefers-reduced-motion`;
- fallback para conteúdo revelado quando o JavaScript ou o observer não estão disponíveis;
- quebra segura de textos longos e prevenção de sobreposição em painéis finais.

## Evidências e limitações

A extração foi baseada em inspeção pública, captura visual, DOM/acessibilidade, estilos computados, CSS publicado e probes de interação. A página de referência principal foi capturada em `1363 × 936`, DPR 1, com tema dark-lemon e rota pública.

Há duas limitações importantes:

- Não houve captura runtime pareada em viewport estreito; o comportamento mobile foi reconstruído a partir das media queries e representado no relatório.
- A arte original, wordmark, screenshots, avatar e logos de terceiros foram intencionalmente omitidos. O relatório usa espécimes neutros para demonstrar o sistema sem redistribuir conteúdo protegido.

Consulte [`evidence/README.md`](evidence/README.md) para os IDs e o contexto de cada evidência.

## Validação do pacote

O relatório incluído nesta distribuição foi validado com:

- manifesto `design-system.json`: 0 erros e 0 avisos;
- JavaScript inline compilável;
- CSS com chaves balanceadas;
- IDs HTML únicos;
- links internos com destinos existentes;
- 36 botões com nome acessível;
- fallbacks de reveal, clipboard, overflow e layout final;
- isolamento do elemento decorativo do rodapé para evitar cobertura de conteúdo.

## Nota sobre direitos e publicação

Este pacote é uma reconstrução de system design baseada em observação pública. Ele não inclui os ativos protegidos da referência. Antes de publicar uma implementação comercial, substitua os espécimes por identidade própria e confirme os direitos de uso de fontes, imagens, ícones, marcas e conteúdos.

---

**Alethe Agents · living design system extraction**  
Captura e documentação: 13 de agosto de 2026 · escopo público · fidelidade em nível de sistema
