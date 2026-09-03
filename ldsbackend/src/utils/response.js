export const successResponse = (res, data = null, meta = null) => {
  return res.status(200).json({
    success: true,
    meta,
    data,
    error: null
  });
};

export const errorResponse = (res, message, code = "SERVER_ERROR", status = 500) => {
  return res.status(status).json({
    success: false,
    meta: null,
    data: null,
    error: {
      message,
      code
    }
  });
};