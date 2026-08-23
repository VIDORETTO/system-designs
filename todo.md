# Backlog de evolução da skill de Web Design System

Branch de planejamento: codex/design-system-experience-backlog-2026-08-22

## Objetivo

Evoluir a skill atual, mantendo o núcleo evidence-first, para extrair não apenas tokens e componentes, mas também a experiência visual que dá personalidade a um site:

- identidade visual e design DNA;
- elementos-signature e composição;
- vídeos de background, posters, imagens e mídia responsiva;
- canvas, WebGL, SVG animado, Lottie, shaders, texturas e overlays;
- motion como linguagem: propósito, gatilho, timeline, driver, interrupção e fallback;
- relatórios vivos que demonstram os padrões reais;
- validação determinística de evidência, acessibilidade, performance e cobertura.

A implementação deve continuar separando Observed, Computed, Inferred e Recommended. Nenhum vídeo, efeito ou comportamento deve ser inventado só porque seria visualmente interessante.

## Princípios de execução

1. Compatibilidade primeiro: manifests existentes continuam válidos.
2. Evidência antes de abstração: cada claim material recebe origem, confiança e limitações.
3. Extração não é redesign: recomendações ficam separadas do sistema observado.
4. Elementos únicos podem ser assinatura visual; tokens e componentes só devem ser abstraídos quando há repetição ou intenção sistêmica.
5. Background video é opcional: só deve ser recomendado quando combina com o modo da superfície e há uma justificativa de experiência.
6. A documentação deve demonstrar o sistema, não apenas listar valores.
7. Toda mídia e efeito precisa de fallback, estratégia de acessibilidade e nota de performance.
8. Protected content não é redistribuído sem autorização; usar poster, frame abstrato ou espécime neutro quando necessário.

## Mapa de fases

| Fase | Resultado principal | Prioridade | Dependências |
| --- | --- | --- | --- |
| 0. Baseline e contrato | Compatibilidade, versionamento e fixtures de referência | P0 | Nenhuma |
| 1. Experience Layer | Identidade, modos, assinatura e regras visuais | P0 | Fase 0 |
| 2. Aquisição de mídia e efeitos | Probes, inventário de assets e composição por camadas | P0 | Fase 0 |
| 3. Normalização de motion e comportamento | Schema rico para motion, mídia, efeitos e elementos | P0 | Fases 1–2 |
| 4. Relatório vivo | Galerias e labs que reproduzem os padrões extraídos | P0 | Fases 1–3 |
| 5. Validação e benchmark | Quality gates, regressões e score de cobertura | P0 | Fases 2–4 |
| 6. Documentação e rollout | Skill, referências, templates e migração documentados | P1 | Fases 0–5 |
| 7. Iteração avançada | Browser live mode, visual diff e asset pipeline avançado | P2 | Fases 4–6 |

## Definition of Done do programa

- Manifests atuais continuam validando sem erro.
- Novos manifests podem representar identidade, elementos, mídia, efeitos e motion.
- Vídeos de background registram poster, playback, crop, fallback, reduced motion e performance.
- Cada motion pattern registra propósito, trigger, propriedades, timing, easing, interrupção e alternativa reduzida.
- O relatório mostra componentes reais com estados e demos específicas de motion/mídia.
- O relatório funciona em desktop e mobile, por teclado e com prefers-reduced-motion.
- Claims principais apontam para evidências e confiança.
- Existem fixtures para landing page, portfolio/experience, dashboard/operate e screenshot/recording-only.
- O validator detecta gaps críticos e não força precisão onde a evidência não existe.
- A documentação explica o que é observado, inferido e recomendado.

---


## Status da implementação nesta branch

Atualizado em 2026-08-23.

- [x] Fases 0–6: contrato v2, Experience Layer, aquisição estática/runtime, mídia, efeitos, motion, renderer, quality gates, fixtures e documentação.
- [x] Fase 7 operacional: picker de elemento, diff visual, extração de frames, export DESIGN.md/sidecar, benchmark de cobertura e auditoria de anti-patterns.
- [x] Fase 8 production hardening: Playwright capture, normal/reduced-motion coverage, browser manifest validator, pixel regression runner, visual baseline policy e GitHub Actions.
- [x] DS-608: PR #1 integrada no main em 2026-08-23.
- [x] DS-705: corpus representativo versionado, benchmark executável e browser capture/visual gate integrados na CI; sites externos entram por configuração autorizada.

Legenda: [x] implementado e validado localmente/na CI · execução de sites externos permanece opt-in e depende de autorização.

# Fase 0 — Baseline, compatibilidade e contrato

## Objetivo

Criar uma base estável para a evolução sem quebrar o schema, o template Alethe ou os scripts atuais.

- [x] DS-000 — Registrar baseline atual
  - Arquivos: skill/SKILL.md, skill/references, skill/scripts, templates/saas/alethe-design-system.
  - Aceite: validação atual, geração do relatório e estrutura do template ficam registradas no README da branch ou em uma nota de benchmark.

- [x] DS-001 — Introduzir versionamento do manifesto
  - Adicionar meta.schema_version sem tornar o campo obrigatório para manifests antigos.
  - Aceite: validator aceita manifests sem versão como versão legada e identifica a versão normalizada quando presente.

- [x] DS-002 — Definir política de compatibilidade
  - Documentar quais campos são mantidos, quais são opcionais e como uma migração será feita.
  - Aceite: existe uma tabela de migração entre o schema atual e a Experience Layer.

- [x] DS-003 — Definir enums e IDs estáveis
  - Enums para surface_mode, media.kind, media.role, effects.driver, motion.job e fallback.
  - Aceite: nomes estão documentados e não dependem de nomes de classe ou framework.

- [x] DS-004 — Criar fixture mínimo da nova camada
  - Adicionar um manifesto pequeno com identity_lock, um elemento-signature, um vídeo observado e um motion pattern.
  - Aceite: fixture valida e contém evidência resolvível, confiança e limitações.

## Gate da fase

O fixture legado Alethe e o fixture novo validam juntos. Nenhuma alteração de schema é implementada sem exemplo válido.

---

# Fase 1 — Experience Layer: identidade e assinatura visual

## Objetivo

Incorporar o melhor do Impeccable sem transformar a extração em redesign: modo da superfície, identidade lock, focal moment e regras nomeadas.

- [x] DS-100 — Adicionar experience.surface_mode
  - Valores: persuade, operate, read, experience.
  - Aceite: SKILL.md explica como o modo muda prioridade de motion, densidade, mídia e interação.

- [x] DS-101 — Adicionar experience.identity_lock
  - Registrar superfície dominante, acento, tipografia, topologia, material, densidade e voz quando observáveis.
  - Aceite: uma frase de identidade pode ser rastreada a evidências e não usa nomes de estilos como conclusão sem dados.

- [x] DS-102 — Adicionar signature_elements
  - Modelar elementos que definem a experiência mesmo quando aparecem uma única vez: hero, marca, cursor, textura, grid, frame, separador, canvas ou tratamento de imagem.
  - Aceite: elementos únicos não são forçados a virar componente reutilizável.

- [x] DS-103 — Adicionar focal_moment
  - Registrar o momento que carrega a personalidade da primeira viewport: mecanismo, escala, posição, trigger e importância.
  - Aceite: o relatório consegue destacar o focal moment e explicar por que ele é significativo.

- [x] DS-104 — Adicionar named_rules, dos e donts
  - Regras curtas, citable e baseadas em evidência ou explicitamente recomendadas.
  - Aceite: toda regra possui basis, confidence e evidence_ids quando não for recomendação.

- [x] DS-105 — Separar sistema observado de oportunidades
  - Criar uma área explícita para oportunidades recomendadas, incluindo mídia ou efeitos que não existem na fonte.
  - Aceite: uma recomendação de background video nunca aparece dentro de tokens observados.

- [x] DS-106 — Atualizar examples.md
  - Incluir exemplos de site Persuade com vídeo, Experience com canvas e Operate sem motion decorativo.
  - Aceite: os exemplos explicam quando não adicionar efeitos.

## Gate da fase

Uma leitura sem assets ou motion ainda produz uma identidade honesta, com gaps explícitos e sem preencher lacunas com estética genérica.

---

# Fase 2 — Aquisição de mídia, elementos e efeitos

## Objetivo

Transformar a coleta de mídia e efeitos em um protocolo repetível, com evidência suficiente para reconstrução.

- [x] DS-200 — Criar probe de inventário de mídia no runtime
  - Detectar img, picture, source, video, audio, canvas, svg, iframe, Lottie e assets carregados dinamicamente.
  - Registrar locator, tipo MIME, dimensões, duração, poster, peso, fonte e status de carregamento.
  - Aceite: o probe distingue conteúdo, decoração, background e mídia de demonstração.

- [x] DS-201 — Criar probe de CSS visual
  - Detectar background-image, gradients, pseudo-elements, masks, clip-path, filter, backdrop-filter, mix-blend-mode, object-fit, object-position, z-index e stacking contexts.
  - Aceite: o relatório consegue explicar a composição por camadas sem depender apenas de screenshot.

- [x] DS-202 — Criar probe de drivers de interação
  - Detectar animation/keyframes, transitions, requestAnimationFrame, IntersectionObserver, listeners de scroll/pointer, animation-timeline e View Transitions quando acessíveis.
  - Aceite: cada driver pode ser classificado como tempo, scroll, pointer, gesture ou state.

- [x] DS-203 — Registrar playback de vídeo
  - Capturar autoplay, muted, loop, playsinline, controls, preload, poster, currentTime, duration e comportamento de pause/resume.
  - Aceite: vídeo decorativo sem áudio e vídeo de conteúdo são diferenciados.

- [x] DS-204 — Capturar filmstrip e frames-chave
  - Para vídeo ou recording autorizado, registrar início, meio, fim, frame de poster e momentos de mudança.
  - Aceite: cada frame possui timestamp, viewport e evidence ID; se não for possível medir, registrar gap.

- [x] DS-205 — Capturar composição do asset
  - Registrar crop, ponto focal, overlay, blend, máscara, camada, proporção e relação com texto/CTA.
  - Aceite: desktop e mobile podem ter regras distintas de crop ou substituição.

- [x] DS-206 — Capturar fallbacks e condições
  - Testar reduced motion, Save-Data quando controlável, mídia bloqueada, rede lenta, viewport estreito e elemento fora da viewport.
  - Aceite: ausência de teste vira gap, nunca comportamento presumido.

- [x] DS-207 — Preservar proveniência e direitos
  - Criar padrão para referenciar asset sem re-hospedar conteúdo protegido; registrar origem, hash ou locator quando permitido.
  - Aceite: report usa poster/placeholder neutro quando a mídia original não pode ser distribuída.

## Gate da fase

Uma página com vídeo, canvas ou textura consegue gerar um inventário de camadas, playback, fallback e limitações. Uma página sem mídia não recebe assets inventados.

---

# Fase 3 — Normalização de elementos, mídia, efeitos e motion

## Objetivo

Expandir o contrato JSON sem duplicar tokens nem misturar comportamento observado com recomendação.

- [x] DS-300 — Adicionar foundations.media ou media.assets
  - Modelar kind, role, locator, poster, intrinsic, playback, composition, responsive, accessibility, performance, basis, confidence e evidence_ids.
  - Aceite: background video possui poster, reduced-motion e estratégia offscreen explícitos.

- [x] DS-301 — Adicionar elements[]
  - Modelar id, kind, role, layer, anatomy, material, geometry, content behavior, tokens_used, responsive_behavior e interaction.
  - Aceite: elementos-signature podem existir sem virar componentes genéricos.

- [x] DS-302 — Adicionar effects[]
  - Modelar kind, target, driver, properties, layering, intensity, trigger, fallback, performance e accessibility.
  - Aceite: parallax, cursor, grain, shader, mask e filter são descritos por propósito e não apenas por tecnologia.

- [x] DS-303 — Enriquecer motion
  - Adicionar thesis, job, driver, trigger, target, phases, duration, delay, stagger, easing, loop, interruption, reversal, scroll range, reduced_motion e performance.
  - Aceite: motion de screenshot recebe candidate/inferred, não easing observado falso.

- [x] DS-304 — Separar timing observado de timing recomendado
  - Registrar raw measurements, measured ranges, source declarations e recommendations em campos diferentes.
  - Aceite: uma duração baseada em frame rate não é apresentada como CSS exato.

- [x] DS-305 — Adicionar media/motion accessibility
  - Registrar aria-hidden, alt, captions, audio policy, focus impact, reduced-motion alternative e state communication.
  - Aceite: o validator sinaliza autoplay sem fallback ou movimento sem alternativa.

- [x] DS-306 — Adicionar performance budget por mídia/efeito
  - Registrar bytes, preload, lazy strategy, offscreen pause, GPU/CPU cost observado e fallback de baixo custo.
  - Aceite: efeitos caros têm estado de risco ou estratégia de degradação.

- [x] DS-307 — Refinar componentes representativos
  - Selecionar 5–10 componentes que expressem a gramática: botão, input, nav, chip, card e assinaturas.
  - Registrar variantes, estados, content rules e snippets self-contained quando possível.
  - Aceite: não extrair wrappers ou one-offs sem intenção repetida.

## Gate da fase

O schema representa tanto um dashboard sem mídia como uma landing page cinematográfica sem exigir campos artificiais em nenhum dos dois casos.

---

# Fase 4 — Relatório vivo e specimen interativo

## Objetivo

Fazer o report.html demonstrar os padrões extraídos, em vez de apenas exibir cards com metadados.

- [x] DS-400 — Adicionar seção Identity & Design DNA
  - Mostrar surface mode, identity lock, focal moment, named rules, dos/donts e limites.
  - Aceite: Observed, Inferred e Recommended são visualmente distinguíveis.

- [x] DS-401 — Adicionar galeria de signature elements
  - Mostrar elemento, papel, camadas, tokens, evidências e responsive behavior.
  - Aceite: a galeria funciona com espécime neutro quando o asset original é protegido.

- [x] DS-402 — Criar component specimen engine
  - Renderizar HTML/CSS real para componentes representativos, com escopo de classes e ícones inline quando aplicável.
  - Demonstrar default, hover, focus-visible, active, disabled, loading e error.
  - Aceite: componentes são alcançáveis por teclado e não são apenas screenshots.

- [x] DS-403 — Criar media lab
  - Mostrar poster, frame strip, metadados de playback, crop, overlays, fallbacks e origem.
  - Aceite: não iniciar áudio; não autoplayar loops de forma perturbadora; oferecer replay e poster.

- [x] DS-404 — Criar effects lab
  - Permitir alternar time, scroll, pointer, static fallback, low-power e reduced-motion.
  - Aceite: remoção do efeito mantém conteúdo e hierarquia legíveis.

- [x] DS-405 — Tornar motion lab específico por pattern
  - Cada padrão tem replay, pause, slow, reduced motion, timeline, properties e evidence IDs.
  - Aceite: eliminar o motion-dot genérico como única demonstração.

- [x] DS-406 — Adicionar responsive comparison
  - Mostrar a mesma região em desktop/mobile, com reflow, hide/show, reorder, replacement, density e crop.
  - Aceite: layout usa media queries reais, não imagem desktop escalada.

- [x] DS-407 — Renderizar accessibility, content_style e performance
  - Mostrar contraste, focus, alt/captions, long-content behavior, localization, autoplay policy e budgets.
  - Aceite: falhas da fonte permanecem visíveis como source findings; não são corrigidas silenciosamente.

- [x] DS-408 — Melhorar evidence viewer
  - Permitir filtrar por evidence ID, viewport, estado, timestamp e fonte.
  - Aceite: cada claim principal leva ao contexto da evidência ou ao gap.

- [x] DS-409 — Expandir exports
  - Exportar CSS variables para tokens, motion, media e effects; opcionalmente gerar uma narrativa DESIGN.md.
  - Aceite: valores recomendados não entram no export observado sem rótulo.

## Gate da fase

O relatório usa os tokens extraídos em seu próprio shell, mostra os estados principais e pode ser verificado por teclado, mobile e reduced motion.

---

# Fase 5 — Validator, detectores e benchmark

## Objetivo

Reduzir falsos positivos e impedir que extrações incompletas sejam chamadas de prontas.

- [x] DS-500 — Validar novos enums e estruturas
  - Verificar experience, elements, media, effects e motion.
  - Aceite: IDs, evidence_ids, basis e confidence são validados recursivamente.

- [x] DS-501 — Criar quality gates específicos de mídia
  - Sinalizar autoplay sem muted, video sem poster/fallback, ausência de mobile strategy, ausência de reduced-motion ou preload sem justificativa.
  - Aceite: o warning explica impacto e como resolver.

- [x] DS-502 — Criar quality gates específicos de motion
  - Sinalizar pattern sem trigger, job, properties, timing, reduced motion ou performance.
  - Aceite: screenshots-only nunca exigem dados impossíveis; devem registrar gap.

- [x] DS-503 — Criar quality gates de componentes
  - Sinalizar componente sem anatomia, estados relevantes, content rules ou foco quando interativo.
  - Aceite: estados não disponíveis são gaps, não valores inventados.

- [x] DS-504 — Criar score e severidade P0–P3
  - Separar erros bloqueadores, gaps maiores, inconsistências menores e polish.
  - Aceite: o resultado contém score, evidências, falsos positivos possíveis e próximos passos.

- [x] DS-505 — Criar fixtures de regressão
  - Landing com background video; portfolio com canvas/pointer; dashboard sem mídia decorativa; screenshot-only; recording-only; mídia inacessível/protegida.
  - Aceite: todos validam com os warnings esperados e outputs estáveis.

- [x] DS-506 — Testar renderer e HTML
  - Verificar JSON embutido, CSS balanceado, IDs únicos, links, clipboard fallback, focus, overflow e scripts.
  - Aceite: geração repetida produz HTML válido e navegável.

- [x] DS-507 — Verificar viewports e estados
  - Renderizar 390×844, 768×1024 quando relevante e 1440×900; testar keyboard e prefers-reduced-motion.
  - Aceite: cada viewport inspecionado aparece no handoff.

- [x] DS-508 — Criar benchmark de cobertura
  - Medir tokens com evidência, componentes com estados, motion com timing, mídia com fallback e claims sem provenance.
  - Aceite: a evolução da skill pode ser comparada entre versões.

## Gate da fase

O template legado continua com zero erros. Fixtures novos capturam casos difíceis e o validator distingue ausência de evidência de erro real.

---

# Fase 6 — Documentação, templates e rollout

## Objetivo

Tornar a nova capacidade descobrível e reproduzível por outros agentes.

- [x] DS-600 — Atualizar skill/SKILL.md
  - Incluir Experience Layer, inventário de mídia, effects lab, background video protocol e critérios de não-invenção.
  - Aceite: workflow principal aponta para as novas referências na ordem correta.

- [x] DS-601 — Atualizar acquisition-playbook.md
  - Adicionar protocolo de vídeo, filmstrip, camadas, canvas, WebGL, pointer, scroll e condições de fallback.
  - Aceite: cada protocolo possui evidência mínima, limites e stop conditions.

- [x] DS-602 — Atualizar extraction-schema.md
  - Documentar novas estruturas, enums, exemplos e migração.
  - Aceite: schema mantém um exemplo mínimo e um exemplo multimídia completo.

- [x] DS-603 — Atualizar report-spec.md
  - Tornar media lab, effects lab, component specimens e evidence viewer parte da especificação.
  - Aceite: acceptance checklist cobre playback, poster, reduced motion e performance.

- [x] DS-604 — Atualizar examples.md
  - Incluir casos de vídeo observado, vídeo recomendado, canvas, screenshot-only e source/runtime disagreement.
  - Aceite: exemplos mostram respostas honestas para gaps.

- [x] DS-605 — Atualizar templates
  - Expandir o template Alethe sem quebrar seu pacote e criar ao menos um fixture media/portfolio.
  - Aceite: README do template explica direitos, assets neutros e como abrir o report.

- [x] DS-606 — Atualizar README raiz e metadata
  - Explicar o novo escopo, exemplos de invocação e outputs.
  - Aceite: a descrição curta da skill menciona media, motion e visual effects sem prometer clonagem.

- [x] DS-607 — Criar changelog/migration guide
  - Registrar versão do schema, compatibilidade, comandos de validação e diferenças do report.
  - Aceite: um usuário consegue atualizar um manifesto existente seguindo apenas o guia.

- [x] DS-608 — Preparar release/PR
  - Resumir mudanças, fixtures, gates, limitações e decisões de direitos.
  - Aceite: PR inclui screenshots do report em desktop/mobile e resultado do validator.

## Gate da fase

Outra pessoa consegue executar a skill, entender o novo schema, validar um fixture multimídia e distinguir fatos observados de recomendações.

---

# Fase 7 — Iteração avançada opcional

Estas tarefas só entram depois dos gates anteriores.

- [x] DS-700 — Browser live mode com element picker
  - Selecionar um elemento, mostrar identidade extraída e gerar variantes no overlay.
  - Não substituir o fluxo de extração evidence-first.

- [x] DS-701 — Visual diff e focal-moment review
  - Comparar screenshots pareados e medir diferenças por região sem prometer pixel perfection.
  - Aceite: comparação identifica material differences e mantém evidência.

- [x] DS-702 — Pipeline de thumbnails/filmstrips
  - Gerar frames de vídeo e previews de assets quando ffmpeg ou ferramenta equivalente estiver disponível.
  - Aceite: fallback apenas com metadata se a ferramenta não existir.

- [x] DS-703 — Export opcional para DESIGN.md + sidecar
  - Produzir narrativa durável, tokens portáteis e extensões para motion/media/effects.
  - Aceite: frontmatter não duplica o JSON e a fonte de verdade é explícita.

- [x] DS-704 — Detector de anti-patterns de documentação
  - Sinalizar relatório neutro demais, componente sem estados, media sem fallback, claims sem evidence e shell que não usa tokens.
  - Aceite: detector explica o problema e evita juízo estético genérico.

- [x] DS-705 — Benchmark em sites representativos
  - Comparar cobertura em marketing, portfolio, editorial, dashboard, ecommerce e media.
  - Aceite: registrar tempo, cobertura, gaps, warnings e falsos positivos.

---

# Critérios de decisão para background video

Só registrar como Recommended quando:

- a superfície é Persuade ou Experience, ou o vídeo tem função comprovadamente informativa;
- existe um ganho claro de hierarquia, atmosfera ou demonstração;
- há poster, fallback estático e estratégia mobile;
- autoplay é muted, playsinline e sem áudio intrusivo;
- reduced motion e Save-Data possuem alternativa;
- a mídia pode ser carregada e pausada com custo aceitável;
- o usuário pediu evolução visual ou há evidência de que a categoria comporta esse recurso.

Nunca:

- inventar que o site usa vídeo sem evidência;
- redistribuir vídeo, logo, imagem ou copy protegidos;
- esconder conteúdo essencial atrás do vídeo;
- usar vídeo para compensar ausência de hierarquia;
- impor WebGL, shader ou parallax a interfaces Operate/Read sem propósito.

# Referências de implementação

- Skill atual: skill/SKILL.md
- Aquisição: skill/references/acquisition-playbook.md
- Schema: skill/references/extraction-schema.md
- Relatório: skill/references/report-spec.md
- Validator: skill/scripts/validate_design_system.py
- Renderer: skill/scripts/render_design_system_report.py
- Fixture principal: templates/saas/alethe-design-system
- Impeccable document flow: https://github.com/pbakaus/impeccable/blob/main/skill/reference/document.md
- Impeccable extract flow: https://github.com/pbakaus/impeccable/blob/main/skill/reference/extract.md
- Impeccable motion guidance: https://github.com/pbakaus/impeccable/blob/main/skill/reference/animate.md
- Impeccable advanced effects: https://github.com/pbakaus/impeccable/blob/main/skill/reference/overdrive.md
- Impeccable visual/asset workflow: https://github.com/pbakaus/impeccable/blob/main/skill/reference/visualize.md

# Próximo passo recomendado

Implementar DS-000 até DS-004, depois DS-100 até DS-106, antes de alterar o renderer. Isso estabiliza o contrato e evita construir demos para um schema que ainda não foi decidido.
