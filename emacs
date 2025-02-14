;; Added by Package.el.  This must come before configurations of
;; installed packages.  Don't delete this line.  If you don't want it,
;; just comment it out by adding a semicolon to the start of the line.
;; You may delete these explanatory comments.
(require 'package)
(let* ((no-ssl (and (memq system-type '(windows-nt ms-dos))
                    (not (gnutls-available-p))))
       (proto (if no-ssl "http" "https")))
  (when no-ssl
    (warn "\
Your version of Emacs does not support SSL connections,
which is unsafe because it allows man-in-the-middle attacks.
There are two things you can do about this warning:
1. Install an Emacs version that does support SSL and be safe.
2. Remove this warning from your init file so you won't see it again."))
  ;; Comment/uncomment these two lines to enable/disable MELPA and MELPA Stable as desired
  (add-to-list 'package-archives (cons "melpa" (concat proto "://melpa.org/packages/")) t)
  ;;(add-to-list 'package-archives (cons "melpa-stable" (concat proto "://stable.melpa.org/packages/")) t)
  (when (< emacs-major-version 24)
    ;; For important compatibility libraries like cl-lib
    (add-to-list 'package-archives (cons "gnu" (concat proto "://elpa.gnu.org/packages/")))))
(package-initialize)

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(custom-enabled-themes (quote (wombat)))
 '(package-selected-packages
   (quote
    (monokai-theme python-environment python pippel pip-requirements pipenv hy-mode company-ycm company-ghci company-box browse-at-remote biblio bazel-mode cmake-ide elpy company-try-hard company-shell company-c-headers company-anaconda tile test-c spotify projectile outrespace org-gnome org neotree mongo highlight git gh flycheck-haskell flycheck-inline flycheck-golangci-lint flycheck-clojure flycheck-clangcheck flycheck-clang-tidy flycheck-clang-analyzer flycheck dad-joke company-php company-ngram company-math company-lua company-go company-bibtex company dash-functional dash))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
(require 'package)

;; Company auto completion
(add-hook 'after-init-hook 'global-company-mode)
(add-hook 'after-init-hook #'global-flycheck-mode)
(eval-after-load "company"
  '(add-to-list 'company-backends '(company-anaconda :with company-capf)))
(add-hook 'python-mode-hook 'anaconda-mode)
(elpy-enable)
;; Enable line numbers
(when (version<= "26.0.50" emacs-version)
  (global-display-line-numbers-mode))
(load-theme 'monokai t)
