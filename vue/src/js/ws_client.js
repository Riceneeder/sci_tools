import { io } from "socket.io-client";

/**
 * A WebSocket client class for managing WebSocket connections and handling events.
 *
 * @class WsClient
 * @classdesc This class provides methods to connect to a WebSocket server, send messages, and handle incoming messages and connection events.
 * 
 * @property {Socket|null} socket - The Socket.IO instance.
 * @property {string} url - The URL to which to connect.
 * @property {Map<string, Function>} events - A map of event names to their corresponding callback functions.
 * 
 * @example
 * const client = new WsClient('http://localhost:5000');
 * client.connect();
 * client.on('message', (data) => {
 *   console.log(data);
 * });
 * client.send('message', { text: 'Hello, World!' });
 */
class WsClient {
  /**
   * Creates an instance of the WebSocket client.
   * 
   * @constructor
   * @param {string} url - The URL to which to connect.
   */
  constructor(url) {
    this.url = url;
    this.socket = null;
    this.events = new Map();
  }

  /**
   * Establishes a WebSocket connection to the specified URL and sets up event handlers.
   * 
   * @method connect
   * @memberof WsClient
   * @this {WsClient}
   */
  connect() {
    this.socket = io(this.url,{
      extraHeaders:{
        'Access-Control-Allow-Origin':'*'
      },
      // transports: ['websocket']
    });
    this.socket.on('connect', this.onOpen.bind(this));
    this.socket.on('disconnect', this.onClose.bind(this));
  }

  /**
   * Event handler for when the WebSocket connection is opened.
   * Logs a message indicating the connection URL.
   */
  onOpen() {
    console.log("Connected to " + this.url);
  }

  /**
   * Event handler for when the WebSocket connection is closed.
   * Logs a message to the console indicating that the connection has been closed.
   */
  onClose() {
    console.log("Connection closed");
  }

  /**
   * Sends a message through the WebSocket connection.
   *
   * @param {string} event - The event type to send.
   * @param {Object} payload - The data to send with the event.
   */
  send(event, payload) {
    this.socket.emit('message', { event, payload });
  }

  /**
   * Registers an event listener for the specified event.
   *
   * @param {string} eventName - The name of the event to listen for.
   * @param {Function} callback - The callback function to execute when the event is triggered.
   */
  on(eventName, callback) {
    // this.events.set(eventName, callback);
    this.socket.on(eventName, callback);
  }
}

export default WsClient;