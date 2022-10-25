// Setup your project to serve `py-worker.js`. You should also serve
// `pyodide.js`, and all its associated `.asm.js`, `.data`, `.json`,
// and `.wasm` files as well:
importScripts("https://cdn.jsdelivr.net/pyodide/v0.21.3/full/pyodide.js");

async function loadPyodideAndPackages() {
  self.pyodide = await loadPyodide({
    stdin: () => { return ""; },
    stdout: (s) => { console.log(s); },
    stderr: (s) => { console.log(s); }
  });
  await self.pyodide.loadPackage(["numpy", "js", "micropip"]);//packages including js module
  self.micropip = pyodide.pyimport("micropip");
}
let pyodideReadyPromise = loadPyodideAndPackages();

// N.B. Input blocks so beware
self.onmessage = async (event) => {
  // make sure loading is done
  await pyodideReadyPromise;
  // Don't bother yet with this line, suppose our API is built in such a way:
  const { callback, python, ...context } = event.data;
  // The worker copies the context in its own "memory" (an object mapping name to values)
  for (const key of Object.keys(context)) {
    self[key] = context[key];
  }
  // Now is the easy part, the one that is similar to working in the main thread:
  try {
    await self.pyodide.loadPackagesFromImports(python);
    let results = await self.pyodide.runPythonAsync(python);
    self.postMessage({ results, callback });
  } catch (error) {
    self.postMessage({ error: error.message, callback });
  }
};