export const splitIntoClauses = (text) => {
  if (!text) return [];

  return text
    .split(/\n|\./)
    .map(c => c.trim())
    .filter(c => c.length > 20);
};