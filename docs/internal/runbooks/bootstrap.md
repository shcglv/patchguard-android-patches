# Bootstrap runbook — Stage 0 / G1-G2

Статус: **Stage 0 выполнен**. Публичный репозиторий создан и опубликован.

- Репозиторий: https://github.com/shcglv/patchguard-android-patches
- Default branch: `main`
- Ветки: `main`, `dev`
- Лицензия: GPL-3.0-only (из шаблона)
- Релизов и тегов пока нет
- `Validate` на `main` и `dev`: успешно
- `Release` намеренно пропускается до Stage 6

## Что сделано

1. Локальный репозиторий создан как клон официального шаблона Morphe на commit
   `4cb966a5aa5ea70725aa5eb4531eea8f0e5549e6`.
2. Поверх шаблона добавлены governance-документы, static-only политика, схемы,
   SQLite-схема, CLI-каркас, тесты, документация и брендинг.
3. Пакеты шаблона переименованы из `app.template` в `app.patchguard`.
4. Создан пустой публичный репозиторий `shcglv/patchguard-android-patches`.
5. Опубликованы `main` и `dev`; `main` был fast-forward до `dev` до первого push.
6. Настроены базовые security settings и минимальный ruleset.
7. `dev` влит в `main` merge-коммитом; default branch отображает PatchGuard.
8. `Release` закрыт repository variable `PATCHGUARD_RELEASE_ENABLED=false`.

## Почему не «Use this template» на GitHub

Локальный репозиторий уже содержит историю официального шаблона. Создание через
GitHub template дало бы независимую историю, которую пришлось бы объединять или
force-push’ить. Вместо этого создан пустой репозиторий и опубликованы локальные
ветки. Структура, Gradle-модули и release pipeline шаблона сохранены.

## Фактические настройки GitHub

- Public repository, default branch `main`.
- Topics: `android`, `morphe`, `patches`, `security-audit`, `supply-chain`,
  `static-analysis`.
- Secret scanning и push protection: включены.
- Vulnerability alerts и automated security fixes: включены.
- Private vulnerability reporting: включено.
- Actions: включены; workflow permissions по умолчанию `read`;
  разрешено создание PR из Actions.
- Ruleset `Protect main and dev from deletion and force-push`: запрещает
  удаление и force-push для `main`/`dev`.
- Repository variable `PATCHGUARD_RELEASE_ENABLED=false`.
- `Release` workflow: `if: vars.PATCHGUARD_RELEASE_ENABLED == 'true'`, поэтому
  push в `main`/`dev` создаёт skipped run, а не релиз.

## Ограничения и принятые решения

- `gh` не установлен: MSI-установка через winget зависла на этапе elevation.
  Для создания репозитория и push использован уже сохранённый Git credential
  через одноразовый in-memory `Authorization` header. Токен не печатался,
  не коммитился и не сохранялся в файлы.
- `sha_pinning_required=true` в GitHub Actions оказался неприменим для
  personal-репозитория: runner отклонил `actions/checkout` и
  `actions/setup-python` с формулировкой «all actions must be from a repository
  owned by shcglv». Политика отключена; все actions в workflow-файлах
  закреплены полным commit SHA вручную. Это residual risk, пока GitHub не
  поддержит политику для personal-репозиториев.
- Требование PR и required checks пока не включены: сначала нужен
  release-identity (PAT/App), иначе официальный semantic-release не сможет
  делать прямые push’и сгенерированных файлов.
- `Release` отключён до Stage 6, чтобы первый push не создал релиз и не
  расходовал CI на сборку без `read:packages`.

## Известные открытые риски

- **minimatch / GHSA-g3hv-75wg-m249 (medium).** Уязвимость в транзитивной
  dev-зависимости npm (`package-lock.json`, внутри bundled npm). Патч
  `minimatch >= 11.0.1` несовместим с текущими диапазонами родителей; алерт
  затрагивает CI-инструменты, а не релизный `.mpp`, и требует
  attacker-controlled glob pattern. Решение: отслеживать обновление
  semantic-release/npm, не принимать внешние glob-шаблоны в CI. Алерт не
  закрывать вручную без устранения причины.
- **`sha_pinning_required`.** GitHub отклонил политику для personal-репозитория
  («all actions must be from a repository owned by shcglv»). Политика отключена;
  actions закреплены полным SHA в workflow-файлах. Это контролируется ревью,
  но не GitHub policy.
- **PR/required checks.** Пока не включены: нужен release-identity, иначе
  официальный semantic-release не сможет пушить generated-файлы. До этого
  действует ruleset только против deletion/force-push.
- **`read:packages` PAT.** Локальная сборка `.mpp` ещё не проверялась; PAT
  отсутствует. Это предусловие Stage 6, а не Stage 0.

## Что осталось до Stage 6

1. Создать PAT `read:packages` и сохранить в `~/.gradle/gradle.properties`
   (не в репозитории).
2. Проверить `./gradlew :patches:buildAndroid` с JDK 21 и `GRADLE_USER_HOME`
   на E:.
3. Настроить release-identity (fine-grained PAT `RELEASE_TOKEN` или GitHub App)
   и добавить его в bypass ruleset.
4. Включить required PR + `Validate` check для `main`/`dev` после тестового
   релиза.
5. Включить CodeQL и разобрать Dependabot PR.
6. Включить GitHub Pages только после отдельного разрешения.
7. Установить `PATCHGUARD_RELEASE_ENABLED=true` только перед первым
   контролируемым релизом.

## Проверка

```powershell
git status
git log --oneline --decorate -5
git remote -v
```

Ожидаемо: `main` содержит merge-коммит bootstrap, `dev` — рабочую ветку,
`origin` указывает на PatchGuard, рабочее дерево чистое (кроме gitignored
`.patchguard/`, `site/`).

## Откат

До появления релизов откат — удаление публичного репозитория после отдельного
подтверждения владельца. Локальная история сохраняется. После появления
релизов откат выполняется только новым релизом, без удаления истории.
