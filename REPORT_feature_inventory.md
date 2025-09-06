# Zimmer User Panel — Feature Inventory

**Generated**: 06/09/2025, 11:11:53 PM
**Pages Analyzed**: 16
**Routes Found**: 16
**Desired Features**: 16
**Covered Features**: 2
**Missing Features**: 14

## 📄 Pages Scanned

### /

### /_app
- **Components**: AppProps, AuthProvider, HeaderAuth

### /automations
- **Components**: DashboardLayout, QuickActions, MyAutomationsList

### /automations/[id]/purchase
- **Title**: اتوماسیون یافت نشد
- **Endpoints**: `/api/automations/${id}`, `/api/discounts/validate`, `/api/payments/zarinpal/init`
- **Actions**: form/buttons detected
- **Components**: Head, DiscountCodeField, PriceSummary

### /automations/marketplace
- **Components**: DashboardLayout, Card

### /dashboard
- **Actions**: form/buttons detected
- **Components**: DashboardLayout, RecentPayments, MyAutomations

### /forgot-password
- **Title**: فراموشی رمز عبور
- **Actions**: form/buttons detected
- **Links**: /login
- **Components**: Link, ApiClient

### /login
- **Title**: Zimmer AI
- **Actions**: form/buttons detected
- **Links**: /signup, /forgot-password
- **Components**: Link, TwoFADialog, Toast

### /payment
- **Components**: DashboardLayout, ActiveAutomations

### /reset-password
- **Title**: بازنشانی رمز عبور
- **Actions**: form/buttons detected
- **Links**: /login
- **Components**: Link, ApiClient

### /settings
- **Title**: تنظیمات حساب کاربری
- **Actions**: form/buttons detected
- **Links**: /settings/security
- **Components**: DashboardLayout, ProfileForm

### /settings/security
- **Title**: امنیت حساب
- **Endpoints**: `/api/auth/2fa/status`, `/api/auth/2fa/initiate`, `/api/auth/2fa/activate`, `/api/auth/2fa/disable`, `/api/auth/2fa/recovery-codes/regenerate`
- **Actions**: form/buttons detected

### /signup
- **Title**: Zimmer AI
- **Actions**: form/buttons detected
- **Links**: /login
- **Components**: React, Link

### /support
- **Title**: پشتیبانی
- **Actions**: form/buttons detected
- **Components**: DashboardLayout, Card

### /test
- **Title**: Test Page

### /verify-email
- **Title**: تأیید ایمیل
- **Actions**: form/buttons detected
- **Links**: /login

## 🗺️ Feature Map by Route

### /
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: —

### /_app
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: AppProps, AuthProvider, HeaderAuth

### /automations
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: DashboardLayout, QuickActions, MyAutomationsList

### /automations/[id]/purchase
- **Endpoints**: `/api/automations/${id}`, `/api/discounts/validate`, `/api/payments/zarinpal/init`
- **Methods**: POST, GET?
- **Charts**: —
- **Components**: Head, DiscountCodeField, PriceSummary

### /automations/marketplace
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: DashboardLayout, Card

### /dashboard
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: DashboardLayout, RecentPayments, MyAutomations

### /forgot-password
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: Link, ApiClient

### /login
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: Link, TwoFADialog, Toast

### /payment
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: DashboardLayout, ActiveAutomations

### /reset-password
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: Link, ApiClient

### /settings
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: DashboardLayout, ProfileForm

### /settings/security
- **Endpoints**: `/api/auth/2fa/status`, `/api/auth/2fa/initiate`, `/api/auth/2fa/activate`, `/api/auth/2fa/disable`, `/api/auth/2fa/recovery-codes/regenerate`
- **Methods**: POST, GET?
- **Charts**: —
- **Components**: —

### /signup
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: React, Link

### /support
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: DashboardLayout, Card

### /test
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: —

### /verify-email
- **Endpoints**: —
- **Methods**: —
- **Charts**: —
- **Components**: —

## 🎯 Desired Feature Coverage

- ❌ **ویرایش پروفایل** (`auth.profile`)

- ❌ **امنیت حساب (۲مرحله‌ای/ایمیل)** (`auth.security`)

- ❌ **تاریخچه پرداخت** (`payments.history`)

- ❌ **نمودار هزینه‌های ماهانه** (`payments.monthly`)

- ✅ **خرید اعتبار/توکن** (`payments.purchase`)
  - **Routes**: /automations/[id]/purchase
  - **Endpoints**: `/api/payments/zarinpal/init`

- ✅ **کد تخفیف** (`discounts`)
  - **Routes**: /automations/[id]/purchase
  - **Endpoints**: `/api/discounts/validate`, `/api/payments/zarinpal/init`

- ❌ **فهرست اتوماسیون‌های من** (`automations.list`)

- ❌ **جزئیات اتوماسیون** (`automations.detail`)

- ❌ **مصرف هفتگی** (`usage.weekly`)

- ❌ **مصرف ۶ ماه اخیر** (`usage.sixMonths`)

- ❌ **توزیع مصرف بین اتوماسیون‌ها** (`usage.distribution`)

- ❌ **اعلان‌ها** (`notifications`)

- ❌ **تیکت‌ها** (`support.tickets`)

- ❌ **مستندات/هلپ** (`help.docs`)

- ❌ **دسترسی API/توکن‌ها** (`api.dev`)

- ❌ **یکپارچه‌سازی‌ها/سلامت** (`integrations`)

## ❌ Missing Desired Features

These features are defined in the desired feature list but not found on any page:

- ❌ **ویرایش پروفایل** (`auth.profile`)
- ❌ **امنیت حساب (۲مرحله‌ای/ایمیل)** (`auth.security`)
- ❌ **تاریخچه پرداخت** (`payments.history`)
- ❌ **نمودار هزینه‌های ماهانه** (`payments.monthly`)
- ❌ **فهرست اتوماسیون‌های من** (`automations.list`)
- ❌ **جزئیات اتوماسیون** (`automations.detail`)
- ❌ **مصرف هفتگی** (`usage.weekly`)
- ❌ **مصرف ۶ ماه اخیر** (`usage.sixMonths`)
- ❌ **توزیع مصرف بین اتوماسیون‌ها** (`usage.distribution`)
- ❌ **اعلان‌ها** (`notifications`)
- ❌ **تیکت‌ها** (`support.tickets`)
- ❌ **مستندات/هلپ** (`help.docs`)
- ❌ **دسترسی API/توکن‌ها** (`api.dev`)
- ❌ **یکپارچه‌سازی‌ها/سلامت** (`integrations`)

## 🔄 Endpoint Overlap Analysis

- *(No endpoint overlaps found)*

## 📊 Summary Statistics

- **Total Unique Endpoints**: 8
- **Total Unique Components**: 19
- **Total Chart Types**: 0
- **Feature Coverage Rate**: 13%
