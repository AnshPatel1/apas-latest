!function () {
    var t = {
        8764: function (t) {
            t.exports = function () {
                "use strict";
                var t = {
                    awaitingPromise: new WeakMap,
                    promise: new WeakMap,
                    innerParams: new WeakMap,
                    domCache: new WeakMap
                };
                const e = t => {
                        const e = {};
                        for (const n in t) e[t[n]] = "swal2-" + t[n];
                        return e
                    },
                    n = e(["container", "shown", "height-auto", "iosfix", "popup", "modal", "no-backdrop", "no-transition", "toast", "toast-shown", "show", "hide", "close", "title", "html-container", "actions", "confirm", "deny", "cancel", "default-outline", "footer", "icon", "icon-content", "image", "input", "file", "range", "select", "radio", "checkbox", "label", "textarea", "inputerror", "input-label", "validation-message", "progress-steps", "active-progress-step", "progress-step", "progress-step-line", "loader", "loading", "styled", "top", "top-start", "top-end", "top-left", "top-right", "center", "center-start", "center-end", "center-left", "center-right", "bottom", "bottom-start", "bottom-end", "bottom-left", "bottom-right", "grow-row", "grow-column", "grow-fullscreen", "rtl", "timer-progress-bar", "timer-progress-bar-container", "scrollbar-measure", "icon-success", "icon-warning", "icon-info", "icon-question", "icon-error", "no-war"]),
                    o = e(["success", "warning", "info", "question", "error"]), i = "SweetAlert2:",
                    r = t => t.charAt(0).toUpperCase() + t.slice(1), s = t => {
                        console.warn("".concat(i, " ").concat("object" == typeof t ? t.join(" ") : t))
                    }, a = t => {
                        console.error("".concat(i, " ").concat(t))
                    }, c = [], l = (t, e) => {
                        var n;
                        n = '"'.concat(t, '" is deprecated and will be removed in the next major release. Please use "').concat(e, '" instead.'), c.includes(n) || (c.push(n), s(n))
                    }, u = t => "function" == typeof t ? t() : t, d = t => t && "function" == typeof t.toPromise,
                    p = t => d(t) ? t.toPromise() : Promise.resolve(t), m = t => t && Promise.resolve(t) === t,
                    g = () => document.body.querySelector(".".concat(n.container)), h = t => {
                        const e = g();
                        return e ? e.querySelector(t) : null
                    }, f = t => h(".".concat(t)), b = () => f(n.popup), y = () => f(n.icon), w = () => f(n.title),
                    v = () => f(n["html-container"]), C = () => f(n.image), A = () => f(n["progress-steps"]),
                    k = () => f(n["validation-message"]), P = () => h(".".concat(n.actions, " .").concat(n.confirm)),
                    B = () => h(".".concat(n.actions, " .").concat(n.deny)), x = () => h(".".concat(n.loader)),
                    E = () => h(".".concat(n.actions, " .").concat(n.cancel)), T = () => f(n.actions),
                    S = () => f(n.footer), L = () => f(n["timer-progress-bar"]), O = () => f(n.close), M = () => {
                        const t = Array.from(b().querySelectorAll('[tabindex]:not([tabindex="-1"]):not([tabindex="0"])')).sort(((t, e) => {
                                const n = parseInt(t.getAttribute("tabindex")), o = parseInt(e.getAttribute("tabindex"));
                                return n > o ? 1 : n < o ? -1 : 0
                            })),
                            e = Array.from(b().querySelectorAll('\n  a[href],\n  area[href],\n  input:not([disabled]),\n  select:not([disabled]),\n  textarea:not([disabled]),\n  button:not([disabled]),\n  iframe,\n  object,\n  embed,\n  [tabindex="0"],\n  [contenteditable],\n  audio[controls],\n  video[controls],\n  summary\n')).filter((t => "-1" !== t.getAttribute("tabindex")));
                        return (t => {
                            const e = [];
                            for (let n = 0; n < t.length; n++) -1 === e.indexOf(t[n]) && e.push(t[n]);
                            return e
                        })(t.concat(e)).filter((t => $(t)))
                    },
                    j = () => q(document.body, n.shown) && !q(document.body, n["toast-shown"]) && !q(document.body, n["no-backdrop"]),
                    H = () => b() && q(b(), n.toast), I = {previousBodyPadding: null}, D = (t, e) => {
                        if (t.textContent = "", e) {
                            const n = (new DOMParser).parseFromString(e, "text/html");
                            Array.from(n.querySelector("head").childNodes).forEach((e => {
                                t.appendChild(e)
                            })), Array.from(n.querySelector("body").childNodes).forEach((e => {
                                t.appendChild(e)
                            }))
                        }
                    }, q = (t, e) => {
                        if (!e) return !1;
                        const n = e.split(/\s+/);
                        for (let e = 0; e < n.length; e++) if (!t.classList.contains(n[e])) return !1;
                        return !0
                    }, V = (t, e, i) => {
                        if (((t, e) => {
                            Array.from(t.classList).forEach((i => {
                                Object.values(n).includes(i) || Object.values(o).includes(i) || Object.values(e.showClass).includes(i) || t.classList.remove(i)
                            }))
                        })(t, e), e.customClass && e.customClass[i]) {
                            if ("string" != typeof e.customClass[i] && !e.customClass[i].forEach) return s("Invalid type of customClass.".concat(i, '! Expected string or iterable object, got "').concat(typeof e.customClass[i], '"'));
                            U(t, e.customClass[i])
                        }
                    }, N = (t, e) => {
                        if (!e) return null;
                        switch (e) {
                            case"select":
                            case"textarea":
                            case"file":
                                return t.querySelector(".".concat(n.popup, " > .").concat(n[e]));
                            case"checkbox":
                                return t.querySelector(".".concat(n.popup, " > .").concat(n.checkbox, " input"));
                            case"radio":
                                return t.querySelector(".".concat(n.popup, " > .").concat(n.radio, " input:checked")) || t.querySelector(".".concat(n.popup, " > .").concat(n.radio, " input:first-child"));
                            case"range":
                                return t.querySelector(".".concat(n.popup, " > .").concat(n.range, " input"));
                            default:
                                return t.querySelector(".".concat(n.popup, " > .").concat(n.input))
                        }
                    }, R = t => {
                        if (t.focus(), "file" !== t.type) {
                            const e = t.value;
                            t.value = "", t.value = e
                        }
                    }, F = (t, e, n) => {
                        t && e && ("string" == typeof e && (e = e.split(/\s+/).filter(Boolean)), e.forEach((e => {
                            Array.isArray(t) ? t.forEach((t => {
                                n ? t.classList.add(e) : t.classList.remove(e)
                            })) : n ? t.classList.add(e) : t.classList.remove(e)
                        })))
                    }, U = (t, e) => {
                        F(t, e, !0)
                    }, _ = (t, e) => {
                        F(t, e, !1)
                    }, W = (t, e) => {
                        const n = Array.from(t.children);
                        for (let t = 0; t < n.length; t++) {
                            const o = n[t];
                            if (o instanceof HTMLElement && q(o, e)) return o
                        }
                    }, z = (t, e, n) => {
                        n === "".concat(parseInt(n)) && (n = parseInt(n)), n || 0 === parseInt(n) ? t.style[e] = "number" == typeof n ? "".concat(n, "px") : n : t.style.removeProperty(e)
                    }, K = function (t) {
                        let e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : "flex";
                        t.style.display = e
                    }, Y = t => {
                        t.style.display = "none"
                    }, Z = (t, e, n, o) => {
                        const i = t.querySelector(e);
                        i && (i.style[n] = o)
                    }, X = function (t, e) {
                        e ? K(t, arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : "flex") : Y(t)
                    }, $ = t => !(!t || !(t.offsetWidth || t.offsetHeight || t.getClientRects().length)),
                    J = t => !!(t.scrollHeight > t.clientHeight), G = t => {
                        const e = window.getComputedStyle(t),
                            n = parseFloat(e.getPropertyValue("animation-duration") || "0"),
                            o = parseFloat(e.getPropertyValue("transition-duration") || "0");
                        return n > 0 || o > 0
                    }, Q = function (t) {
                        let e = arguments.length > 1 && void 0 !== arguments[1] && arguments[1];
                        const n = L();
                        $(n) && (e && (n.style.transition = "none", n.style.width = "100%"), setTimeout((() => {
                            n.style.transition = "width ".concat(t / 1e3, "s linear"), n.style.width = "0%"
                        }), 10))
                    }, tt = {}, et = t => new Promise((e => {
                        if (!t) return e();
                        const n = window.scrollX, o = window.scrollY;
                        tt.restoreFocusTimeout = setTimeout((() => {
                            tt.previousActiveElement instanceof HTMLElement ? (tt.previousActiveElement.focus(), tt.previousActiveElement = null) : document.body && document.body.focus(), e()
                        }), 100), window.scrollTo(n, o)
                    })), nt = () => "undefined" == typeof window || "undefined" == typeof document,
                    ot = '\n <div aria-labelledby="'.concat(n.title, '" aria-describedby="').concat(n["html-container"], '" class="').concat(n.popup, '" tabindex="-1">\n   <button type="button" class="').concat(n.close, '"></button>\n   <ul class="').concat(n["progress-steps"], '"></ul>\n   <div class="').concat(n.icon, '"></div>\n   <img class="').concat(n.image, '" />\n   <h2 class="').concat(n.title, '" id="').concat(n.title, '"></h2>\n   <div class="').concat(n["html-container"], '" id="').concat(n["html-container"], '"></div>\n   <input class="').concat(n.input, '" />\n   <input type="file" class="').concat(n.file, '" />\n   <div class="').concat(n.range, '">\n     <input type="range" />\n     <output></output>\n   </div>\n   <select class="').concat(n.select, '"></select>\n   <div class="').concat(n.radio, '"></div>\n   <label for="').concat(n.checkbox, '" class="').concat(n.checkbox, '">\n     <input type="checkbox" />\n     <span class="').concat(n.label, '"></span>\n   </label>\n   <textarea class="').concat(n.textarea, '"></textarea>\n   <div class="').concat(n["validation-message"], '" id="').concat(n["validation-message"], '"></div>\n   <div class="').concat(n.actions, '">\n     <div class="').concat(n.loader, '"></div>\n     <button type="button" class="').concat(n.confirm, '"></button>\n     <button type="button" class="').concat(n.deny, '"></button>\n     <button type="button" class="').concat(n.cancel, '"></button>\n   </div>\n   <div class="').concat(n.footer, '"></div>\n   <div class="').concat(n["timer-progress-bar-container"], '">\n     <div class="').concat(n["timer-progress-bar"], '"></div>\n   </div>\n </div>\n').replace(/(^|\n)\s*/g, ""),
                    it = () => {
                        tt.currentInstance.resetValidationMessage()
                    }, rt = t => {
                        const e = (() => {
                            const t = g();
                            return !!t && (t.remove(), _([document.documentElement, document.body], [n["no-backdrop"], n["toast-shown"], n["has-column"]]), !0)
                        })();
                        if (nt()) return void a("SweetAlert2 requires document to initialize");
                        const o = document.createElement("div");
                        o.className = n.container, e && U(o, n["no-transition"]), D(o, ot);
                        const i = "string" == typeof (r = t.target) ? document.querySelector(r) : r;
                        var r;
                        i.appendChild(o), (t => {
                            const e = b();
                            e.setAttribute("role", t.toast ? "alert" : "dialog"), e.setAttribute("aria-live", t.toast ? "polite" : "assertive"), t.toast || e.setAttribute("aria-modal", "true")
                        })(t), (t => {
                            "rtl" === window.getComputedStyle(t).direction && U(g(), n.rtl)
                        })(i), (() => {
                            const t = b(), e = W(t, n.input), o = W(t, n.file),
                                i = t.querySelector(".".concat(n.range, " input")),
                                r = t.querySelector(".".concat(n.range, " output")), s = W(t, n.select),
                                a = t.querySelector(".".concat(n.checkbox, " input")), c = W(t, n.textarea);
                            e.oninput = it, o.onchange = it, s.onchange = it, a.onchange = it, c.oninput = it, i.oninput = () => {
                                it(), r.value = i.value
                            }, i.onchange = () => {
                                it(), r.value = i.value
                            }
                        })()
                    }, st = (t, e) => {
                        t instanceof HTMLElement ? e.appendChild(t) : "object" == typeof t ? at(t, e) : t && D(e, t)
                    }, at = (t, e) => {
                        t.jquery ? ct(e, t) : D(e, t.toString())
                    }, ct = (t, e) => {
                        if (t.textContent = "", 0 in e) for (let n = 0; n in e; n++) t.appendChild(e[n].cloneNode(!0)); else t.appendChild(e.cloneNode(!0))
                    }, lt = (() => {
                        if (nt()) return !1;
                        const t = document.createElement("div"),
                            e = {WebkitAnimation: "webkitAnimationEnd", animation: "animationend"};
                        for (const n in e) if (Object.prototype.hasOwnProperty.call(e, n) && void 0 !== t.style[n]) return e[n];
                        return !1
                    })(), ut = (t, e) => {
                        const o = T(), i = x();
                        e.showConfirmButton || e.showDenyButton || e.showCancelButton ? K(o) : Y(o), V(o, e, "actions"), function (t, e, o) {
                            const i = P(), r = B(), s = E();
                            dt(i, "confirm", o), dt(r, "deny", o), dt(s, "cancel", o), function (t, e, o, i) {
                                if (!i.buttonsStyling) return _([t, e, o], n.styled);
                                U([t, e, o], n.styled), i.confirmButtonColor && (t.style.backgroundColor = i.confirmButtonColor, U(t, n["default-outline"])), i.denyButtonColor && (e.style.backgroundColor = i.denyButtonColor, U(e, n["default-outline"])), i.cancelButtonColor && (o.style.backgroundColor = i.cancelButtonColor, U(o, n["default-outline"]))
                            }(i, r, s, o), o.reverseButtons && (o.toast ? (t.insertBefore(s, i), t.insertBefore(r, i)) : (t.insertBefore(s, e), t.insertBefore(r, e), t.insertBefore(i, e)))
                        }(o, i, e), D(i, e.loaderHtml), V(i, e, "loader")
                    };

                function dt(t, e, o) {
                    X(t, o["show".concat(r(e), "Button")], "inline-block"), D(t, o["".concat(e, "ButtonText")]), t.setAttribute("aria-label", o["".concat(e, "ButtonAriaLabel")]), t.className = n[e], V(t, o, "".concat(e, "Button")), U(t, o["".concat(e, "ButtonClass")])
                }

                const pt = (t, e) => {
                    const o = g();
                    o && (function (t, e) {
                        "string" == typeof e ? t.style.background = e : e || U([document.documentElement, document.body], n["no-backdrop"])
                    }(o, e.backdrop), function (t, e) {
                        e in n ? U(t, n[e]) : (s('The "position" parameter is not valid, defaulting to "center"'), U(t, n.center))
                    }(o, e.position), function (t, e) {
                        if (e && "string" == typeof e) {
                            const o = "grow-".concat(e);
                            o in n && U(t, n[o])
                        }
                    }(o, e.grow), V(o, e, "container"))
                };
                const mt = ["input", "file", "range", "select", "radio", "checkbox", "textarea"], gt = t => {
                    if (!Ct[t.input]) return a('Unexpected type of input! Expected "text", "email", "password", "number", "tel", "select", "radio", "checkbox", "textarea", "file" or "url", got "'.concat(t.input, '"'));
                    const e = wt(t.input), n = Ct[t.input](e, t);
                    K(e), setTimeout((() => {
                        R(n)
                    }))
                }, ht = (t, e) => {
                    const n = N(b(), t);
                    if (n) {
                        (t => {
                            for (let e = 0; e < t.attributes.length; e++) {
                                const n = t.attributes[e].name;
                                ["type", "value", "style"].includes(n) || t.removeAttribute(n)
                            }
                        })(n);
                        for (const t in e) n.setAttribute(t, e[t])
                    }
                }, ft = t => {
                    const e = wt(t.input);
                    "object" == typeof t.customClass && U(e, t.customClass.input)
                }, bt = (t, e) => {
                    t.placeholder && !e.inputPlaceholder || (t.placeholder = e.inputPlaceholder)
                }, yt = (t, e, o) => {
                    if (o.inputLabel) {
                        t.id = n.input;
                        const i = document.createElement("label"), r = n["input-label"];
                        i.setAttribute("for", t.id), i.className = r, "object" == typeof o.customClass && U(i, o.customClass.inputLabel), i.innerText = o.inputLabel, e.insertAdjacentElement("beforebegin", i)
                    }
                }, wt = t => W(b(), n[t] || n.input), vt = (t, e) => {
                    ["string", "number"].includes(typeof e) ? t.value = "".concat(e) : m(e) || s('Unexpected type of inputValue! Expected "string", "number" or "Promise", got "'.concat(typeof e, '"'))
                }, Ct = {};
                Ct.text = Ct.email = Ct.password = Ct.number = Ct.tel = Ct.url = (t, e) => (vt(t, e.inputValue), yt(t, t, e), bt(t, e), t.type = e.input, t), Ct.file = (t, e) => (yt(t, t, e), bt(t, e), t), Ct.range = (t, e) => {
                    const n = t.querySelector("input"), o = t.querySelector("output");
                    return vt(n, e.inputValue), n.type = e.input, vt(o, e.inputValue), yt(n, t, e), t
                }, Ct.select = (t, e) => {
                    if (t.textContent = "", e.inputPlaceholder) {
                        const n = document.createElement("option");
                        D(n, e.inputPlaceholder), n.value = "", n.disabled = !0, n.selected = !0, t.appendChild(n)
                    }
                    return yt(t, t, e), t
                }, Ct.radio = t => (t.textContent = "", t), Ct.checkbox = (t, e) => {
                    const o = N(b(), "checkbox");
                    o.value = "1", o.id = n.checkbox, o.checked = Boolean(e.inputValue);
                    const i = t.querySelector("span");
                    return D(i, e.inputPlaceholder), o
                }, Ct.textarea = (t, e) => {
                    vt(t, e.inputValue), bt(t, e), yt(t, t, e);
                    return setTimeout((() => {
                        if ("MutationObserver" in window) {
                            const e = parseInt(window.getComputedStyle(b()).width);
                            new MutationObserver((() => {
                                const n = t.offsetWidth + (o = t, parseInt(window.getComputedStyle(o).marginLeft) + parseInt(window.getComputedStyle(o).marginRight));
                                var o;
                                b().style.width = n > e ? "".concat(n, "px") : null
                            })).observe(t, {attributes: !0, attributeFilter: ["style"]})
                        }
                    })), t
                };
                const At = (e, o) => {
                    const i = v();
                    V(i, o, "htmlContainer"), o.html ? (st(o.html, i), K(i, "block")) : o.text ? (i.textContent = o.text, K(i, "block")) : Y(i), ((e, o) => {
                        const i = b(), r = t.innerParams.get(e), s = !r || o.input !== r.input;
                        mt.forEach((t => {
                            const e = W(i, n[t]);
                            ht(t, o.inputAttributes), e.className = n[t], s && Y(e)
                        })), o.input && (s && gt(o), ft(o))
                    })(e, o)
                }, kt = (t, e) => {
                    for (const n in o) e.icon !== n && _(t, o[n]);
                    U(t, o[e.icon]), xt(t, e), Pt(), V(t, e, "icon")
                }, Pt = () => {
                    const t = b(), e = window.getComputedStyle(t).getPropertyValue("background-color"),
                        n = t.querySelectorAll("[class^=swal2-success-circular-line], .swal2-success-fix");
                    for (let t = 0; t < n.length; t++) n[t].style.backgroundColor = e
                }, Bt = (t, e) => {
                    let n, o = t.innerHTML;
                    e.iconHtml ? n = Et(e.iconHtml) : "success" === e.icon ? (n = '\n  <div class="swal2-success-circular-line-left"></div>\n  <span class="swal2-success-line-tip"></span> <span class="swal2-success-line-long"></span>\n  <div class="swal2-success-ring"></div> <div class="swal2-success-fix"></div>\n  <div class="swal2-success-circular-line-right"></div>\n', o = o.replace(/ style=".*?"/g, "")) : n = "error" === e.icon ? '\n  <span class="swal2-x-mark">\n    <span class="swal2-x-mark-line-left"></span>\n    <span class="swal2-x-mark-line-right"></span>\n  </span>\n' : Et({
                        question: "?",
                        warning: "!",
                        info: "i"
                    }[e.icon]), o.trim() !== n.trim() && D(t, n)
                }, xt = (t, e) => {
                    if (e.iconColor) {
                        t.style.color = e.iconColor, t.style.borderColor = e.iconColor;
                        for (const n of [".swal2-success-line-tip", ".swal2-success-line-long", ".swal2-x-mark-line-left", ".swal2-x-mark-line-right"]) Z(t, n, "backgroundColor", e.iconColor);
                        Z(t, ".swal2-success-ring", "borderColor", e.iconColor)
                    }
                }, Et = t => '<div class="'.concat(n["icon-content"], '">').concat(t, "</div>"), Tt = (t, e) => {
                    t.className = "".concat(n.popup, " ").concat($(t) ? e.showClass.popup : ""), e.toast ? (U([document.documentElement, document.body], n["toast-shown"]), U(t, n.toast)) : U(t, n.modal), V(t, e, "popup"), "string" == typeof e.customClass && U(t, e.customClass), e.icon && U(t, n["icon-".concat(e.icon)])
                }, St = t => {
                    const e = document.createElement("li");
                    return U(e, n["progress-step"]), D(e, t), e
                }, Lt = t => {
                    const e = document.createElement("li");
                    return U(e, n["progress-step-line"]), t.progressStepsDistance && z(e, "width", t.progressStepsDistance), e
                }, Ot = (e, i) => {
                    ((t, e) => {
                        const n = g(), o = b();
                        e.toast ? (z(n, "width", e.width), o.style.width = "100%", o.insertBefore(x(), y())) : z(o, "width", e.width), z(o, "padding", e.padding), e.color && (o.style.color = e.color), e.background && (o.style.background = e.background), Y(k()), Tt(o, e)
                    })(0, i), pt(0, i), ((t, e) => {
                        const o = A();
                        if (!e.progressSteps || 0 === e.progressSteps.length) return Y(o);
                        K(o), o.textContent = "", e.currentProgressStep >= e.progressSteps.length && s("Invalid currentProgressStep parameter, it should be less than progressSteps.length (currentProgressStep like JS arrays starts from 0)"), e.progressSteps.forEach(((t, i) => {
                            const r = St(t);
                            if (o.appendChild(r), i === e.currentProgressStep && U(r, n["active-progress-step"]), i !== e.progressSteps.length - 1) {
                                const t = Lt(e);
                                o.appendChild(t)
                            }
                        }))
                    })(0, i), ((e, n) => {
                        const i = t.innerParams.get(e), r = y();
                        if (i && n.icon === i.icon) return Bt(r, n), void kt(r, n);
                        if (n.icon || n.iconHtml) {
                            if (n.icon && -1 === Object.keys(o).indexOf(n.icon)) return a('Unknown icon! Expected "success", "error", "warning", "info" or "question", got "'.concat(n.icon, '"')), void Y(r);
                            K(r), Bt(r, n), kt(r, n), U(r, n.showClass.icon)
                        } else Y(r)
                    })(e, i), ((t, e) => {
                        const o = C();
                        if (!e.imageUrl) return Y(o);
                        K(o, ""), o.setAttribute("src", e.imageUrl), o.setAttribute("alt", e.imageAlt), z(o, "width", e.imageWidth), z(o, "height", e.imageHeight), o.className = n.image, V(o, e, "image")
                    })(0, i), ((t, e) => {
                        const n = w();
                        X(n, e.title || e.titleText, "block"), e.title && st(e.title, n), e.titleText && (n.innerText = e.titleText), V(n, e, "title")
                    })(0, i), ((t, e) => {
                        const n = O();
                        D(n, e.closeButtonHtml), V(n, e, "closeButton"), X(n, e.showCloseButton), n.setAttribute("aria-label", e.closeButtonAriaLabel)
                    })(0, i), At(e, i), ut(0, i), ((t, e) => {
                        const n = S();
                        X(n, e.footer), e.footer && st(e.footer, n), V(n, e, "footer")
                    })(0, i), "function" == typeof i.didRender && i.didRender(b())
                };

                function Mt() {
                    const e = t.innerParams.get(this);
                    if (!e) return;
                    const o = t.domCache.get(this);
                    Y(o.loader), H() ? e.icon && K(y()) : jt(o), _([o.popup, o.actions], n.loading), o.popup.removeAttribute("aria-busy"), o.popup.removeAttribute("data-loading"), o.confirmButton.disabled = !1, o.denyButton.disabled = !1, o.cancelButton.disabled = !1
                }

                const jt = t => {
                    const e = t.popup.getElementsByClassName(t.loader.getAttribute("data-button-to-replace"));
                    e.length ? K(e[0], "inline-block") : !$(P()) && !$(B()) && !$(E()) && Y(t.actions)
                };
                const Ht = () => P() && P().click(), It = Object.freeze({
                    cancel: "cancel",
                    backdrop: "backdrop",
                    close: "close",
                    esc: "esc",
                    timer: "timer"
                }), Dt = t => {
                    t.keydownTarget && t.keydownHandlerAdded && (t.keydownTarget.removeEventListener("keydown", t.keydownHandler, {capture: t.keydownListenerCapture}), t.keydownHandlerAdded = !1)
                }, qt = (t, e, n) => {
                    const o = M();
                    if (o.length) return (e += n) === o.length ? e = 0 : -1 === e && (e = o.length - 1), o[e].focus();
                    b().focus()
                }, Vt = ["ArrowRight", "ArrowDown"], Nt = ["ArrowLeft", "ArrowUp"], Rt = (e, n, o) => {
                    const i = t.innerParams.get(e);
                    i && (n.isComposing || 229 === n.keyCode || (i.stopKeydownPropagation && n.stopPropagation(), "Enter" === n.key ? Ft(e, n, i) : "Tab" === n.key ? Ut(n, i) : [...Vt, ...Nt].includes(n.key) ? _t(n.key) : "Escape" === n.key && Wt(n, i, o)))
                }, Ft = (t, e, n) => {
                    if (u(n.allowEnterKey) && e.target && t.getInput() && e.target instanceof HTMLElement && e.target.outerHTML === t.getInput().outerHTML) {
                        if (["textarea", "file"].includes(n.input)) return;
                        Ht(), e.preventDefault()
                    }
                }, Ut = (t, e) => {
                    const n = t.target, o = M();
                    let i = -1;
                    for (let t = 0; t < o.length; t++) if (n === o[t]) {
                        i = t;
                        break
                    }
                    t.shiftKey ? qt(0, i, -1) : qt(0, i, 1), t.stopPropagation(), t.preventDefault()
                }, _t = t => {
                    const e = P(), n = B(), o = E();
                    if (document.activeElement instanceof HTMLElement && ![e, n, o].includes(document.activeElement)) return;
                    const i = Vt.includes(t) ? "nextElementSibling" : "previousElementSibling";
                    let r = document.activeElement;
                    for (let t = 0; t < T().children.length; t++) {
                        if (r = r[i], !r) return;
                        if (r instanceof HTMLButtonElement && $(r)) break
                    }
                    r instanceof HTMLButtonElement && r.focus()
                }, Wt = (t, e, n) => {
                    u(e.allowEscapeKey) && (t.preventDefault(), n(It.esc))
                };
                var zt = {swalPromiseResolve: new WeakMap, swalPromiseReject: new WeakMap};
                const Kt = () => {
                        Array.from(document.body.children).forEach((t => {
                            t.hasAttribute("data-previous-aria-hidden") ? (t.setAttribute("aria-hidden", t.getAttribute("data-previous-aria-hidden")), t.removeAttribute("data-previous-aria-hidden")) : t.removeAttribute("aria-hidden")
                        }))
                    }, Yt = () => {
                        const t = navigator.userAgent, e = !!t.match(/iPad/i) || !!t.match(/iPhone/i),
                            n = !!t.match(/WebKit/i);
                        if (e && n && !t.match(/CriOS/i)) {
                            const t = 44;
                            b().scrollHeight > window.innerHeight - t && (g().style.paddingBottom = "".concat(t, "px"))
                        }
                    }, Zt = () => {
                        const t = g();
                        let e;
                        t.ontouchstart = t => {
                            e = Xt(t)
                        }, t.ontouchmove = t => {
                            e && (t.preventDefault(), t.stopPropagation())
                        }
                    }, Xt = t => {
                        const e = t.target, n = g();
                        return !($t(t) || Jt(t) || e !== n && (J(n) || !(e instanceof HTMLElement) || "INPUT" === e.tagName || "TEXTAREA" === e.tagName || J(v()) && v().contains(e)))
                    }, $t = t => t.touches && t.touches.length && "stylus" === t.touches[0].touchType,
                    Jt = t => t.touches && t.touches.length > 1, Gt = () => {
                        null === I.previousBodyPadding && document.body.scrollHeight > window.innerHeight && (I.previousBodyPadding = parseInt(window.getComputedStyle(document.body).getPropertyValue("padding-right")), document.body.style.paddingRight = "".concat(I.previousBodyPadding + (() => {
                            const t = document.createElement("div");
                            t.className = n["scrollbar-measure"], document.body.appendChild(t);
                            const e = t.getBoundingClientRect().width - t.clientWidth;
                            return document.body.removeChild(t), e
                        })(), "px"))
                    };

                function Qt(t, e, o, i) {
                    H() ? se(t, i) : (et(o).then((() => se(t, i))), Dt(tt)), /^((?!chrome|android).)*safari/i.test(navigator.userAgent) ? (e.setAttribute("style", "display:none !important"), e.removeAttribute("class"), e.innerHTML = "") : e.remove(), j() && (null !== I.previousBodyPadding && (document.body.style.paddingRight = "".concat(I.previousBodyPadding, "px"), I.previousBodyPadding = null), (() => {
                        if (q(document.body, n.iosfix)) {
                            const t = parseInt(document.body.style.top, 10);
                            _(document.body, n.iosfix), document.body.style.top = "", document.body.scrollTop = -1 * t
                        }
                    })(), Kt()), _([document.documentElement, document.body], [n.shown, n["height-auto"], n["no-backdrop"], n["toast-shown"]])
                }

                function te(t) {
                    t = oe(t);
                    const e = zt.swalPromiseResolve.get(this), n = ee(this);
                    this.isAwaitingPromise() ? t.isDismissed || (ne(this), e(t)) : n && e(t)
                }

                const ee = e => {
                    const n = b();
                    if (!n) return !1;
                    const o = t.innerParams.get(e);
                    if (!o || q(n, o.hideClass.popup)) return !1;
                    _(n, o.showClass.popup), U(n, o.hideClass.popup);
                    const i = g();
                    return _(i, o.showClass.backdrop), U(i, o.hideClass.backdrop), ie(e, n, o), !0
                };
                const ne = e => {
                    e.isAwaitingPromise() && (t.awaitingPromise.delete(e), t.innerParams.get(e) || e._destroy())
                }, oe = t => void 0 === t ? {
                    isConfirmed: !1,
                    isDenied: !1,
                    isDismissed: !0
                } : Object.assign({isConfirmed: !1, isDenied: !1, isDismissed: !1}, t), ie = (t, e, n) => {
                    const o = g(), i = lt && G(e);
                    "function" == typeof n.willClose && n.willClose(e), i ? re(t, e, o, n.returnFocus, n.didClose) : Qt(t, o, n.returnFocus, n.didClose)
                }, re = (t, e, n, o, i) => {
                    tt.swalCloseEventFinishedCallback = Qt.bind(null, t, n, o, i), e.addEventListener(lt, (function (t) {
                        t.target === e && (tt.swalCloseEventFinishedCallback(), delete tt.swalCloseEventFinishedCallback)
                    }))
                }, se = (t, e) => {
                    setTimeout((() => {
                        "function" == typeof e && e.bind(t.params)(), t._destroy()
                    }))
                };

                function ae(e, n, o) {
                    const i = t.domCache.get(e);
                    n.forEach((t => {
                        i[t].disabled = o
                    }))
                }

                function ce(t, e) {
                    if (t) if ("radio" === t.type) {
                        const n = t.parentNode.parentNode.querySelectorAll("input");
                        for (let t = 0; t < n.length; t++) n[t].disabled = e
                    } else t.disabled = e
                }

                const le = {
                        title: "",
                        titleText: "",
                        text: "",
                        html: "",
                        footer: "",
                        icon: void 0,
                        iconColor: void 0,
                        iconHtml: void 0,
                        template: void 0,
                        toast: !1,
                        showClass: {popup: "swal2-show", backdrop: "swal2-backdrop-show", icon: "swal2-icon-show"},
                        hideClass: {popup: "swal2-hide", backdrop: "swal2-backdrop-hide", icon: "swal2-icon-hide"},
                        customClass: {},
                        target: "body",
                        color: void 0,
                        backdrop: !0,
                        heightAuto: !0,
                        allowOutsideClick: !0,
                        allowEscapeKey: !0,
                        allowEnterKey: !0,
                        stopKeydownPropagation: !0,
                        keydownListenerCapture: !1,
                        showConfirmButton: !0,
                        showDenyButton: !1,
                        showCancelButton: !1,
                        preConfirm: void 0,
                        preDeny: void 0,
                        confirmButtonText: "OK",
                        confirmButtonAriaLabel: "",
                        confirmButtonColor: void 0,
                        denyButtonText: "No",
                        denyButtonAriaLabel: "",
                        denyButtonColor: void 0,
                        cancelButtonText: "Cancel",
                        cancelButtonAriaLabel: "",
                        cancelButtonColor: void 0,
                        buttonsStyling: !0,
                        reverseButtons: !1,
                        focusConfirm: !0,
                        focusDeny: !1,
                        focusCancel: !1,
                        returnFocus: !0,
                        showCloseButton: !1,
                        closeButtonHtml: "&times;",
                        closeButtonAriaLabel: "Close this dialog",
                        loaderHtml: "",
                        showLoaderOnConfirm: !1,
                        showLoaderOnDeny: !1,
                        imageUrl: void 0,
                        imageWidth: void 0,
                        imageHeight: void 0,
                        imageAlt: "",
                        timer: void 0,
                        timerProgressBar: !1,
                        width: void 0,
                        padding: void 0,
                        background: void 0,
                        input: void 0,
                        inputPlaceholder: "",
                        inputLabel: "",
                        inputValue: "",
                        inputOptions: {},
                        inputAutoTrim: !0,
                        inputAttributes: {},
                        inputValidator: void 0,
                        returnInputValueOnDeny: !1,
                        validationMessage: void 0,
                        grow: !1,
                        position: "center",
                        progressSteps: [],
                        currentProgressStep: void 0,
                        progressStepsDistance: void 0,
                        willOpen: void 0,
                        didOpen: void 0,
                        didRender: void 0,
                        willClose: void 0,
                        didClose: void 0,
                        didDestroy: void 0,
                        scrollbarPadding: !0
                    },
                    ue = ["allowEscapeKey", "allowOutsideClick", "background", "buttonsStyling", "cancelButtonAriaLabel", "cancelButtonColor", "cancelButtonText", "closeButtonAriaLabel", "closeButtonHtml", "color", "confirmButtonAriaLabel", "confirmButtonColor", "confirmButtonText", "currentProgressStep", "customClass", "denyButtonAriaLabel", "denyButtonColor", "denyButtonText", "didClose", "didDestroy", "footer", "hideClass", "html", "icon", "iconColor", "iconHtml", "imageAlt", "imageHeight", "imageUrl", "imageWidth", "preConfirm", "preDeny", "progressSteps", "returnFocus", "reverseButtons", "showCancelButton", "showCloseButton", "showConfirmButton", "showDenyButton", "text", "title", "titleText", "willClose"],
                    de = {},
                    pe = ["allowOutsideClick", "allowEnterKey", "backdrop", "focusConfirm", "focusDeny", "focusCancel", "returnFocus", "heightAuto", "keydownListenerCapture"],
                    me = t => Object.prototype.hasOwnProperty.call(le, t), ge = t => -1 !== ue.indexOf(t),
                    he = t => de[t], fe = t => {
                        me(t) || s('Unknown parameter "'.concat(t, '"'))
                    }, be = t => {
                        pe.includes(t) && s('The parameter "'.concat(t, '" is incompatible with toasts'))
                    }, ye = t => {
                        he(t) && l(t, he(t))
                    };
                const we = t => {
                    const e = {};
                    return Object.keys(t).forEach((n => {
                        ge(n) ? e[n] = t[n] : s("Invalid parameter to update: ".concat(n))
                    })), e
                };
                const ve = t => {
                    Ce(t), delete t.params, delete tt.keydownHandler, delete tt.keydownTarget, delete tt.currentInstance
                }, Ce = e => {
                    e.isAwaitingPromise() ? (Ae(t, e), t.awaitingPromise.set(e, !0)) : (Ae(zt, e), Ae(t, e))
                }, Ae = (t, e) => {
                    for (const n in t) t[n].delete(e)
                };
                var ke = Object.freeze({
                    hideLoading: Mt,
                    disableLoading: Mt,
                    getInput: function (e) {
                        const n = t.innerParams.get(e || this), o = t.domCache.get(e || this);
                        return o ? N(o.popup, n.input) : null
                    },
                    close: te,
                    isAwaitingPromise: function () {
                        return !!t.awaitingPromise.get(this)
                    },
                    rejectPromise: function (t) {
                        const e = zt.swalPromiseReject.get(this);
                        ne(this), e && e(t)
                    },
                    handleAwaitingPromise: ne,
                    closePopup: te,
                    closeModal: te,
                    closeToast: te,
                    enableButtons: function () {
                        ae(this, ["confirmButton", "denyButton", "cancelButton"], !1)
                    },
                    disableButtons: function () {
                        ae(this, ["confirmButton", "denyButton", "cancelButton"], !0)
                    },
                    enableInput: function () {
                        ce(this.getInput(), !1)
                    },
                    disableInput: function () {
                        ce(this.getInput(), !0)
                    },
                    showValidationMessage: function (e) {
                        const o = t.domCache.get(this), i = t.innerParams.get(this);
                        D(o.validationMessage, e), o.validationMessage.className = n["validation-message"], i.customClass && i.customClass.validationMessage && U(o.validationMessage, i.customClass.validationMessage), K(o.validationMessage);
                        const r = this.getInput();
                        r && (r.setAttribute("aria-invalid", !0), r.setAttribute("aria-describedby", n["validation-message"]), R(r), U(r, n.inputerror))
                    },
                    resetValidationMessage: function () {
                        const e = t.domCache.get(this);
                        e.validationMessage && Y(e.validationMessage);
                        const o = this.getInput();
                        o && (o.removeAttribute("aria-invalid"), o.removeAttribute("aria-describedby"), _(o, n.inputerror))
                    },
                    getProgressSteps: function () {
                        return t.domCache.get(this).progressSteps
                    },
                    update: function (e) {
                        const n = b(), o = t.innerParams.get(this);
                        if (!n || q(n, o.hideClass.popup)) return s("You're trying to update the closed or closing popup, that won't work. Use the update() method in preConfirm parameter or show a new popup.");
                        const i = we(e), r = Object.assign({}, o, i);
                        Ot(this, r), t.innerParams.set(this, r), Object.defineProperties(this, {
                            params: {
                                value: Object.assign({}, this.params, e),
                                writable: !1,
                                enumerable: !0
                            }
                        })
                    },
                    _destroy: function () {
                        const e = t.domCache.get(this), n = t.innerParams.get(this);
                        n ? (e.popup && tt.swalCloseEventFinishedCallback && (tt.swalCloseEventFinishedCallback(), delete tt.swalCloseEventFinishedCallback), "function" == typeof n.didDestroy && n.didDestroy(), ve(this)) : Ce(this)
                    }
                });
                const Pe = t => {
                        let e = b();
                        e || new En, e = b();
                        const n = x();
                        H() ? Y(y()) : Be(e, t), K(n), e.setAttribute("data-loading", "true"), e.setAttribute("aria-busy", "true"), e.focus()
                    }, Be = (t, e) => {
                        const o = T(), i = x();
                        !e && $(P()) && (e = P()), K(o), e && (Y(e), i.setAttribute("data-button-to-replace", e.className)), i.parentNode.insertBefore(i, e), U([t, o], n.loading)
                    }, xe = t => t.checked ? 1 : 0, Ee = t => t.checked ? t.value : null,
                    Te = t => t.files.length ? null !== t.getAttribute("multiple") ? t.files : t.files[0] : null,
                    Se = (t, e) => {
                        const n = b(), o = t => Oe[e.input](n, Me(t), e);
                        d(e.inputOptions) || m(e.inputOptions) ? (Pe(P()), p(e.inputOptions).then((e => {
                            t.hideLoading(), o(e)
                        }))) : "object" == typeof e.inputOptions ? o(e.inputOptions) : a("Unexpected type of inputOptions! Expected object, Map or Promise, got ".concat(typeof e.inputOptions))
                    }, Le = (t, e) => {
                        const n = t.getInput();
                        Y(n), p(e.inputValue).then((o => {
                            n.value = "number" === e.input ? parseFloat(o) || 0 : "".concat(o), K(n), n.focus(), t.hideLoading()
                        })).catch((e => {
                            a("Error in inputValue promise: ".concat(e)), n.value = "", K(n), n.focus(), t.hideLoading()
                        }))
                    }, Oe = {
                        select: (t, e, o) => {
                            const i = W(t, n.select), r = (t, e, n) => {
                                const i = document.createElement("option");
                                i.value = n, D(i, e), i.selected = je(n, o.inputValue), t.appendChild(i)
                            };
                            e.forEach((t => {
                                const e = t[0], n = t[1];
                                if (Array.isArray(n)) {
                                    const t = document.createElement("optgroup");
                                    t.label = e, t.disabled = !1, i.appendChild(t), n.forEach((e => r(t, e[1], e[0])))
                                } else r(i, n, e)
                            })), i.focus()
                        }, radio: (t, e, o) => {
                            const i = W(t, n.radio);
                            e.forEach((t => {
                                const e = t[0], r = t[1], s = document.createElement("input"),
                                    a = document.createElement("label");
                                s.type = "radio", s.name = n.radio, s.value = e, je(e, o.inputValue) && (s.checked = !0);
                                const c = document.createElement("span");
                                D(c, r), c.className = n.label, a.appendChild(s), a.appendChild(c), i.appendChild(a)
                            }));
                            const r = i.querySelectorAll("input");
                            r.length && r[0].focus()
                        }
                    }, Me = t => {
                        const e = [];
                        return "undefined" != typeof Map && t instanceof Map ? t.forEach(((t, n) => {
                            let o = t;
                            "object" == typeof o && (o = Me(o)), e.push([n, o])
                        })) : Object.keys(t).forEach((n => {
                            let o = t[n];
                            "object" == typeof o && (o = Me(o)), e.push([n, o])
                        })), e
                    }, je = (t, e) => e && e.toString() === t.toString(), He = (e, n) => {
                        const o = t.innerParams.get(e);
                        if (!o.input) return void a('The "input" parameter is needed to be set when using returnInputValueOn'.concat(r(n)));
                        const i = ((t, e) => {
                            const n = t.getInput();
                            if (!n) return null;
                            switch (e.input) {
                                case"checkbox":
                                    return xe(n);
                                case"radio":
                                    return Ee(n);
                                case"file":
                                    return Te(n);
                                default:
                                    return e.inputAutoTrim ? n.value.trim() : n.value
                            }
                        })(e, o);
                        o.inputValidator ? Ie(e, i, n) : e.getInput().checkValidity() ? "deny" === n ? De(e, i) : Ne(e, i) : (e.enableButtons(), e.showValidationMessage(o.validationMessage))
                    }, Ie = (e, n, o) => {
                        const i = t.innerParams.get(e);
                        e.disableInput(), Promise.resolve().then((() => p(i.inputValidator(n, i.validationMessage)))).then((t => {
                            e.enableButtons(), e.enableInput(), t ? e.showValidationMessage(t) : "deny" === o ? De(e, n) : Ne(e, n)
                        }))
                    }, De = (e, n) => {
                        const o = t.innerParams.get(e || void 0);
                        o.showLoaderOnDeny && Pe(B()), o.preDeny ? (t.awaitingPromise.set(e || void 0, !0), Promise.resolve().then((() => p(o.preDeny(n, o.validationMessage)))).then((t => {
                            !1 === t ? (e.hideLoading(), ne(e)) : e.close({isDenied: !0, value: void 0 === t ? n : t})
                        })).catch((t => Ve(e || void 0, t)))) : e.close({isDenied: !0, value: n})
                    }, qe = (t, e) => {
                        t.close({isConfirmed: !0, value: e})
                    }, Ve = (t, e) => {
                        t.rejectPromise(e)
                    }, Ne = (e, n) => {
                        const o = t.innerParams.get(e || void 0);
                        o.showLoaderOnConfirm && Pe(), o.preConfirm ? (e.resetValidationMessage(), t.awaitingPromise.set(e || void 0, !0), Promise.resolve().then((() => p(o.preConfirm(n, o.validationMessage)))).then((t => {
                            $(k()) || !1 === t ? (e.hideLoading(), ne(e)) : qe(e, void 0 === t ? n : t)
                        })).catch((t => Ve(e || void 0, t)))) : qe(e, n)
                    }, Re = (e, n, o) => {
                        n.popup.onclick = () => {
                            const n = t.innerParams.get(e);
                            n && (Fe(n) || n.timer || n.input) || o(It.close)
                        }
                    }, Fe = t => t.showConfirmButton || t.showDenyButton || t.showCancelButton || t.showCloseButton;
                let Ue = !1;
                const _e = t => {
                    t.popup.onmousedown = () => {
                        t.container.onmouseup = function (e) {
                            t.container.onmouseup = void 0, e.target === t.container && (Ue = !0)
                        }
                    }
                }, We = t => {
                    t.container.onmousedown = () => {
                        t.popup.onmouseup = function (e) {
                            t.popup.onmouseup = void 0, (e.target === t.popup || t.popup.contains(e.target)) && (Ue = !0)
                        }
                    }
                }, ze = (e, n, o) => {
                    n.container.onclick = i => {
                        const r = t.innerParams.get(e);
                        Ue ? Ue = !1 : i.target === n.container && u(r.allowOutsideClick) && o(It.backdrop)
                    }
                }, Ke = t => t instanceof Element || (t => "object" == typeof t && t.jquery)(t);
                const Ye = () => {
                    if (tt.timeout) return (() => {
                        const t = L(), e = parseInt(window.getComputedStyle(t).width);
                        t.style.removeProperty("transition"), t.style.width = "100%";
                        const n = e / parseInt(window.getComputedStyle(t).width) * 100;
                        t.style.removeProperty("transition"), t.style.width = "".concat(n, "%")
                    })(), tt.timeout.stop()
                }, Ze = () => {
                    if (tt.timeout) {
                        const t = tt.timeout.start();
                        return Q(t), t
                    }
                };
                let Xe = !1;
                const $e = {};
                const Je = t => {
                    for (let e = t.target; e && e !== document; e = e.parentNode) for (const t in $e) {
                        const n = e.getAttribute(t);
                        if (n) return void $e[t].fire({template: n})
                    }
                };
                var Ge = Object.freeze({
                    isValidParameter: me,
                    isUpdatableParameter: ge,
                    isDeprecatedParameter: he,
                    argsToParams: t => {
                        const e = {};
                        return "object" != typeof t[0] || Ke(t[0]) ? ["title", "html", "icon"].forEach(((n, o) => {
                            const i = t[o];
                            "string" == typeof i || Ke(i) ? e[n] = i : void 0 !== i && a("Unexpected type of ".concat(n, '! Expected "string" or "Element", got ').concat(typeof i))
                        })) : Object.assign(e, t[0]), e
                    },
                    isVisible: () => $(b()),
                    clickConfirm: Ht,
                    clickDeny: () => B() && B().click(),
                    clickCancel: () => E() && E().click(),
                    getContainer: g,
                    getPopup: b,
                    getTitle: w,
                    getHtmlContainer: v,
                    getImage: C,
                    getIcon: y,
                    getInputLabel: () => f(n["input-label"]),
                    getCloseButton: O,
                    getActions: T,
                    getConfirmButton: P,
                    getDenyButton: B,
                    getCancelButton: E,
                    getLoader: x,
                    getFooter: S,
                    getTimerProgressBar: L,
                    getFocusableElements: M,
                    getValidationMessage: k,
                    isLoading: () => b().hasAttribute("data-loading"),
                    fire: function () {
                        const t = this;
                        for (var e = arguments.length, n = new Array(e), o = 0; o < e; o++) n[o] = arguments[o];
                        return new t(...n)
                    },
                    mixin: function (t) {
                        return class extends (this) {
                            _main(e, n) {
                                return super._main(e, Object.assign({}, t, n))
                            }
                        }
                    },
                    showLoading: Pe,
                    enableLoading: Pe,
                    getTimerLeft: () => tt.timeout && tt.timeout.getTimerLeft(),
                    stopTimer: Ye,
                    resumeTimer: Ze,
                    toggleTimer: () => {
                        const t = tt.timeout;
                        return t && (t.running ? Ye() : Ze())
                    },
                    increaseTimer: t => {
                        if (tt.timeout) {
                            const e = tt.timeout.increase(t);
                            return Q(e, !0), e
                        }
                    },
                    isTimerRunning: () => tt.timeout && tt.timeout.isRunning(),
                    bindClickHandler: function () {
                        $e[arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "data-swal-template"] = this, Xe || (document.body.addEventListener("click", Je), Xe = !0)
                    }
                });

                class Qe {
                    constructor(t, e) {
                        this.callback = t, this.remaining = e, this.running = !1, this.start()
                    }

                    start() {
                        return this.running || (this.running = !0, this.started = new Date, this.id = setTimeout(this.callback, this.remaining)), this.remaining
                    }

                    stop() {
                        return this.running && (this.running = !1, clearTimeout(this.id), this.remaining -= (new Date).getTime() - this.started.getTime()), this.remaining
                    }

                    increase(t) {
                        const e = this.running;
                        return e && this.stop(), this.remaining += t, e && this.start(), this.remaining
                    }

                    getTimerLeft() {
                        return this.running && (this.stop(), this.start()), this.remaining
                    }

                    isRunning() {
                        return this.running
                    }
                }

                const tn = ["swal-title", "swal-html", "swal-footer"], en = t => {
                    const e = {};
                    return Array.from(t.querySelectorAll("swal-param")).forEach((t => {
                        ln(t, ["name", "value"]);
                        const n = t.getAttribute("name"), o = t.getAttribute("value");
                        "boolean" == typeof le[n] && "false" === o && (e[n] = !1), "object" == typeof le[n] && (e[n] = JSON.parse(o))
                    })), e
                }, nn = t => {
                    const e = {};
                    return Array.from(t.querySelectorAll("swal-button")).forEach((t => {
                        ln(t, ["type", "color", "aria-label"]);
                        const n = t.getAttribute("type");
                        e["".concat(n, "ButtonText")] = t.innerHTML, e["show".concat(r(n), "Button")] = !0, t.hasAttribute("color") && (e["".concat(n, "ButtonColor")] = t.getAttribute("color")), t.hasAttribute("aria-label") && (e["".concat(n, "ButtonAriaLabel")] = t.getAttribute("aria-label"))
                    })), e
                }, on = t => {
                    const e = {}, n = t.querySelector("swal-image");
                    return n && (ln(n, ["src", "width", "height", "alt"]), n.hasAttribute("src") && (e.imageUrl = n.getAttribute("src")), n.hasAttribute("width") && (e.imageWidth = n.getAttribute("width")), n.hasAttribute("height") && (e.imageHeight = n.getAttribute("height")), n.hasAttribute("alt") && (e.imageAlt = n.getAttribute("alt"))), e
                }, rn = t => {
                    const e = {}, n = t.querySelector("swal-icon");
                    return n && (ln(n, ["type", "color"]), n.hasAttribute("type") && (e.icon = n.getAttribute("type")), n.hasAttribute("color") && (e.iconColor = n.getAttribute("color")), e.iconHtml = n.innerHTML), e
                }, sn = t => {
                    const e = {}, n = t.querySelector("swal-input");
                    n && (ln(n, ["type", "label", "placeholder", "value"]), e.input = n.getAttribute("type") || "text", n.hasAttribute("label") && (e.inputLabel = n.getAttribute("label")), n.hasAttribute("placeholder") && (e.inputPlaceholder = n.getAttribute("placeholder")), n.hasAttribute("value") && (e.inputValue = n.getAttribute("value")));
                    const o = Array.from(t.querySelectorAll("swal-input-option"));
                    return o.length && (e.inputOptions = {}, o.forEach((t => {
                        ln(t, ["value"]);
                        const n = t.getAttribute("value"), o = t.innerHTML;
                        e.inputOptions[n] = o
                    }))), e
                }, an = (t, e) => {
                    const n = {};
                    for (const o in e) {
                        const i = e[o], r = t.querySelector(i);
                        r && (ln(r, []), n[i.replace(/^swal-/, "")] = r.innerHTML.trim())
                    }
                    return n
                }, cn = t => {
                    const e = tn.concat(["swal-param", "swal-button", "swal-image", "swal-icon", "swal-input", "swal-input-option"]);
                    Array.from(t.children).forEach((t => {
                        const n = t.tagName.toLowerCase();
                        e.includes(n) || s("Unrecognized element <".concat(n, ">"))
                    }))
                }, ln = (t, e) => {
                    Array.from(t.attributes).forEach((n => {
                        -1 === e.indexOf(n.name) && s(['Unrecognized attribute "'.concat(n.name, '" on <').concat(t.tagName.toLowerCase(), ">."), "".concat(e.length ? "Allowed attributes are: ".concat(e.join(", ")) : "To set the value, use HTML within the element.")])
                    }))
                }, un = t => {
                    const e = g(), o = b();
                    "function" == typeof t.willOpen && t.willOpen(o);
                    const i = window.getComputedStyle(document.body).overflowY;
                    gn(e, o, t), setTimeout((() => {
                        pn(e, o)
                    }), 10), j() && (mn(e, t.scrollbarPadding, i), Array.from(document.body.children).forEach((t => {
                        t === g() || t.contains(g()) || (t.hasAttribute("aria-hidden") && t.setAttribute("data-previous-aria-hidden", t.getAttribute("aria-hidden")), t.setAttribute("aria-hidden", "true"))
                    }))), H() || tt.previousActiveElement || (tt.previousActiveElement = document.activeElement), "function" == typeof t.didOpen && setTimeout((() => t.didOpen(o))), _(e, n["no-transition"])
                }, dn = t => {
                    const e = b();
                    if (t.target !== e) return;
                    const n = g();
                    e.removeEventListener(lt, dn), n.style.overflowY = "auto"
                }, pn = (t, e) => {
                    lt && G(e) ? (t.style.overflowY = "hidden", e.addEventListener(lt, dn)) : t.style.overflowY = "auto"
                }, mn = (t, e, o) => {
                    (() => {
                        if ((/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream || "MacIntel" === navigator.platform && navigator.maxTouchPoints > 1) && !q(document.body, n.iosfix)) {
                            const t = document.body.scrollTop;
                            document.body.style.top = "".concat(-1 * t, "px"), U(document.body, n.iosfix), Zt(), Yt()
                        }
                    })(), e && "hidden" !== o && Gt(), setTimeout((() => {
                        t.scrollTop = 0
                    }))
                }, gn = (t, e, o) => {
                    U(t, o.showClass.backdrop), e.style.setProperty("opacity", "0", "important"), K(e, "grid"), setTimeout((() => {
                        U(e, o.showClass.popup), e.style.removeProperty("opacity")
                    }), 10), U([document.documentElement, document.body], n.shown), o.heightAuto && o.backdrop && !o.toast && U([document.documentElement, document.body], n["height-auto"])
                };
                var hn = {
                    email: (t, e) => /^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9-]{2,24}$/.test(t) ? Promise.resolve() : Promise.resolve(e || "Invalid email address"),
                    url: (t, e) => /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-z]{2,63}\b([-a-zA-Z0-9@:%_+.~#?&/=]*)$/.test(t) ? Promise.resolve() : Promise.resolve(e || "Invalid URL")
                };

                function fn(t) {
                    (function (t) {
                        t.inputValidator || Object.keys(hn).forEach((e => {
                            t.input === e && (t.inputValidator = hn[e])
                        }))
                    })(t), t.showLoaderOnConfirm && !t.preConfirm && s("showLoaderOnConfirm is set to true, but preConfirm is not defined.\nshowLoaderOnConfirm should be used together with preConfirm, see usage example:\nhttps://sweetalert2.github.io/#ajax-request"), function (t) {
                        (!t.target || "string" == typeof t.target && !document.querySelector(t.target) || "string" != typeof t.target && !t.target.appendChild) && (s('Target parameter is not valid, defaulting to "body"'), t.target = "body")
                    }(t), "string" == typeof t.title && (t.title = t.title.split("\n").join("<br />")), rt(t)
                }

                let bn;

                class yn {
                    constructor() {
                        if ("undefined" == typeof window) return;
                        bn = this;
                        for (var e = arguments.length, n = new Array(e), o = 0; o < e; o++) n[o] = arguments[o];
                        const i = Object.freeze(this.constructor.argsToParams(n));
                        Object.defineProperties(this, {
                            params: {
                                value: i,
                                writable: !1,
                                enumerable: !0,
                                configurable: !0
                            }
                        });
                        const r = bn._main(bn.params);
                        t.promise.set(this, r)
                    }

                    _main(e) {
                        let n = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
                        (t => {
                            !t.backdrop && t.allowOutsideClick && s('"allowOutsideClick" parameter requires `backdrop` parameter to be set to `true`');
                            for (const e in t) fe(e), t.toast && be(e), ye(e)
                        })(Object.assign({}, n, e)), tt.currentInstance && (tt.currentInstance._destroy(), j() && Kt()), tt.currentInstance = bn;
                        const o = vn(e, n);
                        fn(o), Object.freeze(o), tt.timeout && (tt.timeout.stop(), delete tt.timeout), clearTimeout(tt.restoreFocusTimeout);
                        const i = Cn(bn);
                        return Ot(bn, o), t.innerParams.set(bn, o), wn(bn, i, o)
                    }

                    then(e) {
                        return t.promise.get(this).then(e)
                    }

                    finally(e) {
                        return t.promise.get(this).finally(e)
                    }
                }

                const wn = (e, n, o) => new Promise(((i, r) => {
                        const s = t => {
                            e.close({isDismissed: !0, dismiss: t})
                        };
                        zt.swalPromiseResolve.set(e, i), zt.swalPromiseReject.set(e, r), n.confirmButton.onclick = () => {
                            (e => {
                                const n = t.innerParams.get(e);
                                e.disableButtons(), n.input ? He(e, "confirm") : Ne(e, !0)
                            })(e)
                        }, n.denyButton.onclick = () => {
                            (e => {
                                const n = t.innerParams.get(e);
                                e.disableButtons(), n.returnInputValueOnDeny ? He(e, "deny") : De(e, !1)
                            })(e)
                        }, n.cancelButton.onclick = () => {
                            ((t, e) => {
                                t.disableButtons(), e(It.cancel)
                            })(e, s)
                        }, n.closeButton.onclick = () => {
                            s(It.close)
                        }, ((e, n, o) => {
                            t.innerParams.get(e).toast ? Re(e, n, o) : (_e(n), We(n), ze(e, n, o))
                        })(e, n, s), ((t, e, n, o) => {
                            Dt(e), n.toast || (e.keydownHandler = e => Rt(t, e, o), e.keydownTarget = n.keydownListenerCapture ? window : b(), e.keydownListenerCapture = n.keydownListenerCapture, e.keydownTarget.addEventListener("keydown", e.keydownHandler, {capture: e.keydownListenerCapture}), e.keydownHandlerAdded = !0)
                        })(e, tt, o, s), ((t, e) => {
                            "select" === e.input || "radio" === e.input ? Se(t, e) : ["text", "email", "number", "tel", "textarea"].includes(e.input) && (d(e.inputValue) || m(e.inputValue)) && (Pe(P()), Le(t, e))
                        })(e, o), un(o), An(tt, o, s), kn(n, o), setTimeout((() => {
                            n.container.scrollTop = 0
                        }))
                    })), vn = (t, e) => {
                        const n = (t => {
                            const e = "string" == typeof t.template ? document.querySelector(t.template) : t.template;
                            if (!e) return {};
                            const n = e.content;
                            return cn(n), Object.assign(en(n), nn(n), on(n), rn(n), sn(n), an(n, tn))
                        })(t), o = Object.assign({}, le, e, n, t);
                        return o.showClass = Object.assign({}, le.showClass, o.showClass), o.hideClass = Object.assign({}, le.hideClass, o.hideClass), o
                    }, Cn = e => {
                        const n = {
                            popup: b(),
                            container: g(),
                            actions: T(),
                            confirmButton: P(),
                            denyButton: B(),
                            cancelButton: E(),
                            loader: x(),
                            closeButton: O(),
                            validationMessage: k(),
                            progressSteps: A()
                        };
                        return t.domCache.set(e, n), n
                    }, An = (t, e, n) => {
                        const o = L();
                        Y(o), e.timer && (t.timeout = new Qe((() => {
                            n("timer"), delete t.timeout
                        }), e.timer), e.timerProgressBar && (K(o), V(o, e, "timerProgressBar"), setTimeout((() => {
                            t.timeout && t.timeout.running && Q(e.timer)
                        }))))
                    }, kn = (t, e) => {
                        e.toast || (u(e.allowEnterKey) ? Pn(t, e) || qt(0, -1, 1) : Bn())
                    },
                    Pn = (t, e) => e.focusDeny && $(t.denyButton) ? (t.denyButton.focus(), !0) : e.focusCancel && $(t.cancelButton) ? (t.cancelButton.focus(), !0) : !(!e.focusConfirm || !$(t.confirmButton) || (t.confirmButton.focus(), 0)),
                    Bn = () => {
                        document.activeElement instanceof HTMLElement && "function" == typeof document.activeElement.blur && document.activeElement.blur()
                    };
                if ("undefined" != typeof window && /^ru\b/.test(navigator.language) && location.host.match(/\.(ru|su|xn--p1ai)$/) && Math.random() < .1) {
                    const t = document.createElement("div");
                    t.className = "leave-russia-now-and-apply-your-skills-to-the-world";
                    const e = (xn = [{
                        text: "В нижеприведённом видео объясняется как каждый из нас может помочь в том,\n        <strong>чтобы эта бессмысленная и бесчеловечная война остановилась</strong>:",
                        id: "4CfDhaRkw7I"
                    }, {
                        text: "Эмпатия - главное <strong>человеческое</strong> чувство. Способность сопереживать. <strong>Способность поставить себя на место другого.</strong>",
                        id: "s-GLAIY4DXA"
                    }])[Math.floor(Math.random() * xn.length)];
                    D(t, "\n      <div>\n        Если мы не остановим войну, она придет в дом <strong>каждого из нас</strong> и её последствия будут <strong>ужасающими</strong>.\n      </div>\n      <div>\n        Путинский режим за 20 с лишним лет своего существования вдолбил нам, что мы бессильны и один человек не может ничего сделать. <strong>Это не так!</strong>\n      </div>\n      <div>\n        ".concat(e.text, '\n      </div>\n      <iframe width="560" height="315" src="https://www.youtube.com/embed/').concat(e.id, '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n      <div>\n        Нет войне!\n      </div>\n      '));
                    const n = document.createElement("button");
                    n.innerHTML = "&times;", n.onclick = () => t.remove(), t.appendChild(n), window.addEventListener("load", (() => {
                        setTimeout((() => {
                            document.body.appendChild(t)
                        }), 1e3)
                    }))
                }
                var xn;
                Object.assign(yn.prototype, ke), Object.assign(yn, Ge), Object.keys(ke).forEach((t => {
                    yn[t] = function () {
                        if (bn) return bn[t](...arguments)
                    }
                })), yn.DismissReason = It, yn.version = "11.4.33";
                const En = yn;
                return En.default = En, En
            }(), void 0 !== this && this.Sweetalert2 && (this.swal = this.sweetAlert = this.Swal = this.SweetAlert = this.Sweetalert2)
        }
    }, e = {};

    function n(o) {
        var i = e[o];
        if (void 0 !== i) return i.exports;
        var r = e[o] = {exports: {}};
        return t[o].call(r.exports, r, r.exports, n), r.exports
    }

    n.n = function (t) {
        var e = t && t.__esModule ? function () {
            return t.default
        } : function () {
            return t
        };
        return n.d(e, {a: e}), e
    }, n.d = function (t, e) {
        for (var o in e) n.o(e, o) && !n.o(t, o) && Object.defineProperty(t, o, {enumerable: !0, get: e[o]})
    }, n.o = function (t, e) {
        return Object.prototype.hasOwnProperty.call(t, e)
    }, n.r = function (t) {
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, {value: "Module"}), Object.defineProperty(t, "__esModule", {value: !0})
    };
    var o = {};
    !function () {
        "use strict";
        n.r(o), n.d(o, {
            Swal: function () {
                return t
            }
        });
        var t = n(8764).mixin({
            buttonsStyling: !1,
            customClass: {
                confirmButton: "btn btn-primary",
                cancelButton: "btn btn-label-danger",
                denyButton: "btn btn-label-secondary"
            }
        })
    }();
    var i = window;
    for (var r in o) i[r] = o[r];
    o.__esModule && Object.defineProperty(i, "__esModule", {value: !0})
}();