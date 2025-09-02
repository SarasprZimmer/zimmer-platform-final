// CSRF token management utility
class CSRFManager {
  private csrfToken: string | null = null;
  private csrfCookie: string | null = null;

  async getCSRFToken(): Promise<string> {
    if (this.csrfToken) {
      return this.csrfToken;
    }

    try {
      const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${BASE_URL}/api/auth/csrf`, {
        method: 'GET',
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        this.csrfToken = data.csrf_token;
        this.csrfCookie = data.csrf_token; // Store for verification
        return this.csrfToken!;
      } else {
        throw new Error('Failed to get CSRF token');
      }
    } catch (error) {
      console.error('CSRF token fetch error:', error);
      throw error;
    }
  }

  getCSRFHeaders(): HeadersInit {
    if (!this.csrfToken) {
      throw new Error('CSRF token not available. Call getCSRFToken() first.');
    }

    return {
      'X-CSRF-Token': this.csrfToken
    };
  }

  clearCSRFToken(): void {
    this.csrfToken = null;
    this.csrfCookie = null;
  }

  hasCSRFToken(): boolean {
    return !!this.csrfToken;
  }
}

export const csrfManager = new CSRFManager();

// Helper function to get CSRF headers for requests
export async function getCSRFHeaders(): Promise<HeadersInit> {
  if (!csrfManager.hasCSRFToken()) {
    await csrfManager.getCSRFToken();
  }
  return csrfManager.getCSRFHeaders();
}
