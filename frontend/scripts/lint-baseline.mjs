import { readdir, readFile } from 'node:fs/promises'
import { join, relative } from 'node:path'

const rootDir = process.cwd()
const scanRoots = ['src']
const extensions = new Set(['.js', '.vue'])

const checks = [
  { name: 'debugger statement', pattern: /\bdebugger\b/ },
  { name: 'console.log statement', pattern: /console\.log\s*\(/ },
  { name: 'local file URL', pattern: /file:\/\// },
  { name: 'default admin password', pattern: /OneSpirit2026!/ },
  { name: 'demo password token name in frontend source', pattern: /DEMO_(?:USER_)?PASSWORD/ },
  { name: 'JWT secret token name in frontend source', pattern: /JWT_SECRET/ },
  { name: 'database password token name in frontend source', pattern: /DB_PASSWORD/ }
]

const getExtension = (filePath) => {
  const dotIndex = filePath.lastIndexOf('.')
  return dotIndex === -1 ? '' : filePath.slice(dotIndex)
}

async function collectFiles(dir) {
  const entries = await readdir(dir, { withFileTypes: true })
  const files = []

  for (const entry of entries) {
    const fullPath = join(dir, entry.name)
    if (entry.isDirectory()) {
      files.push(...await collectFiles(fullPath))
      continue
    }

    if (entry.isFile() && extensions.has(getExtension(entry.name))) {
      files.push(fullPath)
    }
  }

  return files
}

const failures = []

for (const scanRoot of scanRoots) {
  const files = await collectFiles(join(rootDir, scanRoot))

  for (const file of files) {
    const content = await readFile(file, 'utf8')
    const lines = content.split(/\r?\n/)

    lines.forEach((line, index) => {
      for (const check of checks) {
        if (check.pattern.test(line)) {
          failures.push(`${relative(rootDir, file)}:${index + 1} - ${check.name}`)
        }
      }
    })
  }
}

if (failures.length > 0) {
  console.error('Frontend lint baseline failed:')
  failures.forEach((failure) => console.error(`- ${failure}`))
  process.exit(1)
}

console.log('Frontend lint baseline passed.')
