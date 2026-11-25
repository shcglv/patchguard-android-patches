# Bootstrap runbook — G1/G2

Статус: Stage 0 завершён локально. Публичный репозиторий ещё не создан.

## Что уже готово

- Локальный репозиторий `C:\Users\shcgl\Desktop\morphe` на ветке `dev`.
- История официального шаблона Morphe сохранена; поверх неё один коммит `chore:`.
- Governance-документы, static-only политика, схемы, SQLite-схема, CLI-каркас, тесты и документация.
- `pytest`: 13 passed; `patchguard validate`: OK; `mkdocs build --strict`: OK.
- Локальная БД и `site/` gitignored.

## Почему не «Use this template» на GitHub

Локальный репозиторий уже является клоном официального шаблона на commit
`4cb966a5aa5ea70725aa5eb4531eea8f0e5549e6` с нашей историей. Создание репозитория
через GitHub template дало бы независимую историю, которую пришлось бы
объединять или force-push’ить. Вместо этого создаётся пустой публичный
репозиторий, и в него публикуются локальные ветки. Содержимое, структура и
release pipeline шаблона при этом сохраняются.

## Предусловия

- `gh` установлен и аутентифицирован с доступами `repo`, `workflow`.
- Для локальной сборки `.mpp` — PAT `read:packages` в `~/.gradle/gradle.properties`.
- На C: достаточно места; Gradle home и quarantine — на E:.
- Владелец подтвердил G1 и G2.

## G2: установка и аутентификация

```powershell
winget install --id GitHub.cli --accept-source-agreements --accept-package-agreements
gh auth login --hostname github.com --git-protocol https --scopes repo,workflow,read:packages
gh auth status
```

Если `gh auth login` выполняется в браузере, владелец завершает вход сам.
Токен не передаётся в чат и не коммитится.

## G1: создание пустого репозитория и публикация веток

```powershell
# 1. Создать пустой публичный репозиторий (без README и лицензии).
gh repo create shcglv/patchguard-android-patches --public `
  --description "Independent static-only review catalog and Morphe-compatible patch bundle"

# 2. Переключить remote с шаблона на новый репозиторий.
git remote remove origin
git remote add origin https://github.com/shcglv/patchguard-android-patches.git

# 3. Сделать main равным dev (main — предок dev, fast-forward без force-push).
git checkout main
git merge --ff-only dev
git checkout dev

# 4. Опубликовать main первым, чтобы он стал default branch.
git push -u origin main
git push -u origin dev
```

Проверить:

```powershell
gh repo view shcglv/patchguard-android-patches --web
gh run list --limit 5
git status
```

Ожидаемо: репозиторий публичный, default branch `main`, обе ветки на одном
коммите; Actions запускает `Validate` и `Release` (release не должен создать
релиз, потому что коммит `chore:`).

## Если Release workflow упал

- `Release` на первом push может упасть из-за GitHub Packages authentication
  или Android SDK. Это не блокирует публикацию исходников; зафиксировать лог.
- Не включать branch protection до успешного тестового прогона release.
- Не публиковать релиз вручную.

## После публикации (не входит в этот runbook)

1. Включить secret scanning/push protection, Dependabot, CodeQL, private
   vulnerability reporting.
2. Настроить rulesets и release identity.
3. Включить GitHub Pages.
4. Только после отдельного разрешения — первый `.mpp` pre-release.

## Откат

До появления релизов откат — удаление публичного репозитория после отдельного
подтверждения владельца. Локальная история сохраняется.
