import DOMPurify from "dompurify";

export function sanitize(input: string) {
  return DOMPurify.sanitize(input);
}
