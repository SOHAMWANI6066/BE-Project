export const validatePDFs = (files) => {
  if (!files || files.length === 0) {
    throw new Error("No files uploaded");
  }

  if (files.length > 10) {
    throw new Error("Maximum 10 PDFs allowed");
  }

  files.forEach((file) => {
    if (!file.mimetype.includes("pdf")) {
      throw new Error(`${file.originalname} is not a PDF`);
    }
  });
};