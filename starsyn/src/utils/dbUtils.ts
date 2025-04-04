// src/utils/dbUtils.ts

/**
 * Format error messages from database operations for display
 * @param error Error object caught during database operations
 * @returns Human-readable error message
 */
export function formatDatabaseError(error: unknown): string {
  if (error instanceof Error) {
    // Check for Prisma-specific errors
    if ('code' in error && typeof error.code === 'string') {
      const code = error.code;
      
      // Handle common Prisma error codes
      switch (code) {
        case 'P2001':
          return 'The requested record was not found.';
        case 'P2002':
          return 'A record with this information already exists.';
        case 'P2003':
          return 'Related record not found.';
        case 'P2025':
          return 'Record not found or access denied.';
        default:
          return `Database error: ${error.message}`;
      }
    }
    
    return error.message;
  }
  
  return 'An unknown database error occurred.';
}

/**
 * Log detailed database errors for debugging
 * @param context Description of the operation being performed
 * @param error Error object
 */
export function logDatabaseError(context: string, error: unknown): void {
  console.error(`Database Error (${context}):`, error);
  
  if (error instanceof Error) {
    // Extract specific error details if available
    const details = 'cause' in error ? error.cause : null;
    if (details) {
      console.error('Error details:', details);
    }
    
    // Log stack trace for debugging
    if (error.stack) {
      console.error('Stack trace:', error.stack);
    }
  }
}

/**
 * Safe version of JSON.parse that returns a default value if parsing fails
 * @param data String to parse as JSON
 * @param defaultValue Default value to return if parsing fails
 * @returns Parsed JSON or default value
 */
export function safeJsonParse<T>(data: string, defaultValue: T): T {
  try {
    return JSON.parse(data) as T;
  } catch (error) {
    return defaultValue;
  }
}

/**
 * Checks if a database connection error might be happening
 * @param error Error to analyze
 * @returns True if the error is likely a connection issue
 */
export function isConnectionError(error: unknown): boolean {
  if (error instanceof Error) {
    const message = error.message.toLowerCase();
    
    // Check for common connection error indicators
    return (
      message.includes('connect') && 
      (message.includes('econnrefused') || 
       message.includes('timeout') ||
       message.includes('connection'))
    );
  }
  
  return false;
}
