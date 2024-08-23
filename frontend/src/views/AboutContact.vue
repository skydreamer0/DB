<template>
    <div class="about-contact">
      <h1 class="text-3xl font-bold mb-8">關於我們 & 聯絡我們</h1>
      
      <div class="grid md:grid-cols-2 gap-8">
        <div class="about-section">
          <h2 class="text-2xl font-semibold mb-4">關於我們</h2>
          <p>{{ aboutContent }}</p>
        </div>
        
        <div class="contact-section">
          <h2 class="text-2xl font-semibold mb-4">聯絡我們</h2>
          <ul class="space-y-2">
            <li><strong>地址：</strong>{{ contactInfo.address }}</li>
            <li><strong>電話：</strong>{{ contactInfo.phone }}</li>
            <li><strong>電子郵件：</strong>{{ contactInfo.email }}</li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AboutContactPage',
    data() {
      return {
        aboutContent: '這裡是關於我們的內容。您可以在此處添加公司介紹、使命宣言等信息。',
        contactInfo: {
          address: '台北市某某區某某路123號',
          phone: '(02) 1234-5678',
          email: 'info@example.com'
        }
      };
    }
  };
  </script>
  
  <style scoped>
  .about-contact {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }
  </style>