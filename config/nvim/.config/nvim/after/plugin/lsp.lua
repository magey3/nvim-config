local lsp = require('lsp-zero')

lsp.preset('recommended')

lsp.configure('texlab', {
    settings = {
        texlab = {
            build = {
                executable = "lualatex",
                args = { "-pdf", "-interaction=nonstopmode", "-synctex=1", "%f" },
                forwardSearchAfter = true,
                onSave = true,
            },
            forwardSearch = {
                executable = "evince-synctex",
                args = { "-f", "%l", "%p", "\"code -g %f:%l\"" },
            }
        }
    }
})

lsp.setup()

vim.api.nvim_create_autocmd("BufWrite", {
    pattern = '*.rs',
    callback = vim.lsp.buf.format
})
