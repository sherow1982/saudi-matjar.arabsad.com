/**
 * محرر TinyMCE لمتجر السعودية
 * محرر عربي متخصص للتجارة الإلكترونية في السعودية
 */

// تحميل TinyMCE
function loadTinyMCE() {
  if (window.tinymce) return Promise.resolve();
  
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/tinymce@7/tinymce.min.js';
    script.crossOrigin = 'anonymous';
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

// إعداد محرر المتجر السعودي
function initSaudiMatjarEditor() {
  const config = {
    selector: '.saudi-editor, .product-description, textarea.ksa-text',
    
    plugins: [
      'autolink', 'autoresize', 'autosave', 'charmap', 'directionality',
      'emoticons', 'fullscreen', 'image', 'link', 'lists', 'media',
      'preview', 'quickbars', 'save', 'table', 'visualblocks', 'wordcount'
    ].join(' '),
    
    toolbar: [
      'undo redo | bold italic underline | fontsize',
      'forecolor backcolor | alignleft aligncenter alignright | ltr rtl',
      'bullist numlist | link image table | preview fullscreen | save'
    ].join(' | '),
    
    menubar: 'edit view insert format table',
    
    // إعدادات عربية
    directionality: 'rtl',
    language: 'ar',
    
    height: 400,
    resize: 'vertical',
    
    branding: false,
    promotion: false,
    
    // حفظ تلقائي
    autosave_interval: '30s',
    autosave_retention: '30m',
    
    content_style: `
      body {
        font-family: 'Cairo', 'Noto Sans Arabic', Arial, sans-serif;
        font-size: 15px;
        line-height: 1.7;
        direction: rtl;
        text-align: right;
        color: #2c3e50;
      }
      .ksa-product {
        background: #f8f9fa;
        border: 2px solid #198754;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
      }
      .price-saudi {
        background: linear-gradient(45deg, #198754, #20c997);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        display: inline-block;
      }
      .saudi-badge {
        background: #198754;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
      }
      h1, h2, h3 {
        color: #198754;
        font-weight: bold;
      }
    `,
    
    style_formats: [
      {
        title: 'أنماط المتجر السعودي',
        items: [
          { title: 'بطاقة منتج سعودي', block: 'div', classes: 'ksa-product' },
          { title: 'سعر بالريال', inline: 'span', classes: 'price-saudi' },
          { title: 'شارة سعودية', inline: 'span', classes: 'saudi-badge' },
          { title: 'عنوان رئيسي', block: 'h2', styles: { color: '#198754', 'text-align': 'center' } }
        ]
      }
    ],
    
    setup: function(editor) {
      // زر حفظ منتج سعودي
      editor.ui.registry.addButton('saveSaudiProduct', {
        text: '💾 حفظ KSA',
        tooltip: 'حفظ منتج سعودي',
        onAction: function() {
          const content = editor.getContent();
          const blob = new Blob([`
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منتج من المتجر السعودي</title>
    <style>
        body {
            font-family: 'Cairo', Arial, sans-serif;
            direction: rtl;
            text-align: right;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.7;
            background: #f8f9fa;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .ksa-product {
            background: #f8f9fa;
            border: 2px solid #198754;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }
        .price-saudi {
            background: linear-gradient(45deg, #198754, #20c997);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            text-align: center;
            display: inline-block;
        }
        .saudi-badge {
            background: #198754;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }
        h1, h2, h3 { color: #198754; }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background: #198754;
            color: white;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🇸🇦 منتج من المملكة العربية السعودية</h1>
        ${content}
        
        <div class="footer">
            <p><strong>متجر السعودية</strong></p>
            <p>https://sherow1982.github.io/saudi-matjar.arabsad.com/</p>
            <p>تم الإنشاء: ${new Date().toLocaleDateString('ar-SA')}</p>
        </div>
    </div>
</body>
</html>
          `], { type: 'text/html;charset=utf-8' });
          
          const url = URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = `saudi-product-${Date.now()}.html`;
          link.click();
          URL.revokeObjectURL(url);
          
          editor.notificationManager.open({
            text: 'تم حفظ المنتج السعودي 🇸🇦',
            type: 'success',
            timeout: 3000
          });
        }
      });
      
      // زر إضافة رمز الريال
      editor.ui.registry.addButton('addRiyal', {
        text: 'ر.س',
        tooltip: 'إضافة رمز الريال السعودي',
        onAction: function() {
          editor.insertContent(' ر.س ');
        }
      });
      
      // زر علم السعودية
      editor.ui.registry.addButton('addKSAFlag', {
        text: '🇸🇦',
        tooltip: 'علم المملكة العربية السعودية',
        onAction: function() {
          editor.insertContent('🇸🇦 ');
        }
      });
    }
  };
  
  tinymce.init(config);
}

// تهيئة تلقائية
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    loadTinyMCE().then(initSaudiMatjarEditor).catch(console.error);
  });
} else {
  loadTinyMCE().then(initSaudiMatjarEditor).catch(console.error);
}

// تصدير
window.SaudiMatjarEditor = { loadTinyMCE, initSaudiMatjarEditor };