function t(t) {
    _ = [15, 143, 204, 345, 184, 236, 141, 37, 58, 157, 3, 139, 67, 250, 7, 153, 187, 12, 67, 250, 7, 153, 187, 12, 210, 134, 181, 51, 198, 83, 113];
    о = [165, 174, 189, 118, 80], ο = [114, 175, 131, 129, 217];
    g = (_1 = 345, _2 = 2342, _3 = 0x1337, _4 = 0xDEADBEEF) => {
        e = (function n(_1, _2, _3, _4) {
            return function() {
                var t = _2 << 9,
                    r = _1 * 5;
                r = (r << 7 | r >>> 25) * 9;
                _3 ^= _1;
                _4 ^= _2;
                _2 ^= _3;
                _1 ^= _4;
                _3 ^= t;
                _4 = _4 << 11 | _4 >>> 21;
                return (r >>> 0) / 4294967296;
            };
        })(_1, _2, _3, _4);
        e();
    };
    return (t = ((t) => {
        return t.map(t => {
            const n = t.toString(16);
            return 1 == n.length ? `0${n}` : `${n}`
        }).join("")
    })(((t) => {
        p = t.filter((_, i) => i % 2 == 1);
        q = t.filter((_, i) => i % 2 == 0);
        return [...q.slice(0, Math.floor(q.length / 2)), ...p.slice(Math.floor(p.length / 2)).slice().reverse(), ...p.slice(0, Math.floor(p.length / 2)).slice().concat(p.slice(0, Math.floor(p.length / 2))), ...q.slice(Math.floor(q.length / 2)).slice().reverse()];
    })(Array(((t) => {
        n = [];
        g(0x3, 0o523);
        _j = () => Math.round(e() * t.length) % t.length;
        for (i = 0; i < t.length; i++) {
            ((() => {
                do {
                    j = _j()
                } while (n[j] !== undefined)
            })(), n[j] = t[i])
        };
        return n;
    })(((t) => {
        n = [];
        for (e = 0; e < t.length; e++) {
            n.push(t.charCodeAt(e));
        }
        return n
    })(t))).map(x => [x.slice(0, 5), x.slice(5, 13), x.slice(13, 20), x.slice(20, 25)].map((curr, idx) => ([0, 3].includes(idx) ? ((t, f) => {
        n = [];
        g(0, parseInt("SYKE", 29));
        for (i = 0, j = t.length - 1; i < t.length; i++, j--) {
            (_o = [], o_ = [], (e() > 0.5 ? (() => {
                _o = f ? о : ο;
                o_ = f ? ο : о
            })() : (() => {
                o_ = о;
                _o = ο
            })()), n[j] = t[i] ^ _o[o_[Math.round(e() * o_.length + 1) % o_.length] % _o.length]);
        }
        return n;
    })(curr, idx == 0) : [null, (t) => {
        g();
        n = [];
        for (j = 0; j < t.length; j++) {
            n[t.length - j - 1] = t[j] ^ Math.round(e() * 256);
        }
        return n;
    }, (t) => {
        n = [];
        i = 0;
        for (e = 0; e < t.length; e++) {
            n.push((((e % 4 == 0 ? t[e] - [...о, ...ο][i++ % [...о, ...ο].length] : e % 4 == 1 ? t[e] : e % 4 == 2 ? t[e] + [...о, ...ο][i++ % [...о, ...ο].length] : t[e] ^ [...о, ...ο][i-- % [...о, ...ο].length]) % 256) + 256) % 256);
        }
        return n
    }, null][idx](curr))))[0].flat())))
};

let base = "aaaaaaaaaaaaaaaaaaaaaaaaa";
console.log(t(base))


// various payloads to see what differences there are
let payload = "baaaaaaaaaaaaaaaaaaaaaaaa";
console.log(t(payload));

/*
aaaaaaaaaaaaaaaaaaaaaaaaa - 31b8e01619dccb8131eb30fbc13c42fbc855e13c42fbc855ee0b8e061dc6124
baaaaaaaaaaaaaaaaaaaaaaaa - 31b8e01619dcfb8131eb30fbc13c42fbc855e13c42fbc855ee0b8e061dc6124
caaaaaaaaaaaaaaaaaaaaaaaa - 31b8e01619dceb8131eb30fbc13c42fbc855e13c42fbc855ee0b8e061dc6124
                                        ^ different characters

aaaaaaaaaaaaaaaaaaaaaaaaa - 31b8e01619dccb8131eb30fbc13c42fbc855e13c42fbc855ee0b8e061dc6124
abaaaaaaaaaaaaaaaaaaaaaaa - 31b8e01619dccb8131eb30fbc13c42fbc855e13c42fbc855ee0b8e061dc6224
                                        ^ same characters                               ^ different characters
*/


// brute forcing the flag letter by letter
let alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}_";
let answer = "0f8fcc159b8ec8d253a9d038b43fa0799bb0c43fa0799bb0cd286b533c65371"

for (let i = 0; i < alphabet.length; i++) {
    let payload = alphabet[i]+"aaaaaaaaaaaaaaaaaaaaaaaa";
    result = t(payload);
    if (result.substring(11,13) == answer.substring(11,13)) {
        console.log(payload);
        break;
    }
}




/* FINAL SOLVE SCRIPT */

// the index of the element represents the index of the letter of the flag, and the value of the element represents the index of the modified letter of the output
let modified = [11, 59, 2, 57, 31, 25, 9, 0, 29, 27, 5, 61, 19, 55, 51, 7, 23, 21, 33, 49, 15, 35, 53, 13, 17]

flag = [];
for (let i = 0; i < modified.length; i++) {

    for (let j = 0; j < alphabet.length; j++) {
        let payload = "a".repeat(i)+alphabet[j]+"a".repeat(24-i);
        result = t(payload);

        if (result.substring(modified[i],modified[i]+2) == answer.substring(modified[i],modified[i]+2)) {
            flag.push(alphabet[j]);
            break;
        }
    }

    console.log(flag.join(""));
}