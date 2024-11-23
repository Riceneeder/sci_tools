/**
 * An enumeration of WebSocket event types.
 * @enum {string}
 * @readonly
 */
const WsEvents = Object.freeze({
  PUBLIC_CHANGE: "public_change",
  PDF_CHANGE: "pdf_change",
  MD_CHANGE: "md_change",
  LOG_MESSAGE: "log_message"
});

export default WsEvents;
