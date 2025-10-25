
# Create .gitignore file
gitignore = """# Dependencies
node_modules/
package-lock.json
yarn.lock

# Build files
dist/
build/
*.min.js
*.min.css

# Environment variables
.env
.env.local
.env.production

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Backup files
backup/
*.backup
*.bak
*.old

# Temporary files
tmp/
temp/
*.tmp

# Archives
*.zip
*.rar
*.7z
*.tar.gz

# Design files
*.psd
*.ai
*.sketch
*.fig

# Test files (optional)
test/
tests/
*.test.js
"""

with open('/tmp/.gitignore', 'w', encoding='utf-8') as f:
    f.write(gitignore)

print("✅ تم إنشاء ملف .gitignore")
print("=" * 60)
