// Variables globales
let productos = [];
let registros = [];

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    cargarProductos();
    cargarRegistros();
    actualizarPeso();
    setInterval(actualizarPeso, 500);
});

// Actualizar peso en tiempo real
function actualizarPeso() {
    fetch('/api/peso')
        .then(response => response.json())
        .then(data => {
            const pesoFormato = data.valor.toFixed(3);
            document.getElementById('pesoActual').textContent = pesoFormato;
            document.getElementById('statusBascula').textContent = 'Conectada';
            document.getElementById('statusBascula').style.background = '#4caf50';
        })
        .catch(error => {
            document.getElementById('statusBascula').textContent = 'Desconectada';
            document.getElementById('statusBascula').style.background = '#f44336';
        });
}

// Cargar productos
function cargarProductos() {
    fetch('/api/productos')
        .then(response => response.json())
        .then(data => {
            productos = data;
            mostrarProductos();
            actualizarSelectProductos();
        })
        .catch(error => console.error('Error:', error));
}

// Mostrar productos en grid
function mostrarProductos() {
    const contenedor = document.getElementById('listaProductos');
    
    if (productos.length === 0) {
        contenedor.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #999;">No hay productos registrados</p>';
        return;
    }

    contenedor.innerHTML = productos.map(producto => `
        <div class="producto-card">
            <div class="producto-nombre">${producto.nombre}</div>
            <div class="producto-precio">
                $${producto.precio.toFixed(2)}<span class="producto-precio-label">/kg</span>
            </div>
            <button class="btn-eliminar" onclick="eliminarProducto(${producto.id})">Eliminar</button>
        </div>
    `).join('');
}

// Agregar producto
function agregarProducto() {
    const nombre = document.getElementById('nombreProducto').value.trim();
    const precio = parseFloat(document.getElementById('precioProducto').value);

    if (!nombre || isNaN(precio) || precio <= 0) {
        alert('Por favor completa todos los campos correctamente');
        return;
    }

    fetch('/api/productos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombre, precio })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('nombreProducto').value = '';
        document.getElementById('precioProducto').value = '';
        cargarProductos();
    })
    .catch(error => {
        alert('Error al agregar producto');
        console.error('Error:', error);
    });
}

// Eliminar producto
function eliminarProducto(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar este producto?')) return;

    fetch(`/api/productos/${id}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => cargarProductos())
        .catch(error => {
            alert('Error al eliminar producto');
            console.error('Error:', error);
        });
}

// Actualizar select de productos
function actualizarSelectProductos() {
    const select = document.getElementById('productoSelect');
    const selectedValue = select.value;
    
    select.innerHTML = '<option value="">Seleccionar producto...</option>' +
        productos.map(p => `<option value="${p.id}">${p.nombre}</option>`).join('');
    
    if (selectedValue) {
        select.value = selectedValue;
    }
}

// Registrar pesaje
function registrarPesaje() {
    const productoId = document.getElementById('productoSelect').value;
    const peso = parseFloat(document.getElementById('pesoActual').textContent);

    if (!productoId) {
        alert('Por favor selecciona un producto');
        return;
    }

    if (peso <= 0) {
        alert('El peso debe ser mayor a 0');
        return;
    }

    const producto = productos.find(p => p.id == productoId);

    fetch('/api/registros', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            producto_id: productoId,
            peso: peso,
            precio: producto.precio
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(`Pesaje registrado: $${data.precio_total.toFixed(2)}`);
        cargarRegistros();
    })
    .catch(error => {
        alert('Error al registrar pesaje');
        console.error('Error:', error);
    });
}

// Cargar registros
function cargarRegistros() {
    fetch('/api/registros')
        .then(response => response.json())
        .then(data => {
            registros = data;
            mostrarRegistros();
        })
        .catch(error => console.error('Error:', error));
}

// Mostrar registros en tabla
function mostrarRegistros() {
    const tbody = document.getElementById('historialBody');
    
    if (registros.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #999;">No hay registros</td></tr>';
        return;
    }

    tbody.innerHTML = registros.map(registro => `
        <tr>
            <td><strong>${registro.nombre}</strong></td>
            <td>${parseFloat(registro.peso).toFixed(3)} kg</td>
            <td>$${parseFloat(registro.precio).toFixed(2)}</td>
            <td><strong>$${parseFloat(registro.precio_total).toFixed(2)}</strong></td>
            <td>${registro.fecha}</td>
            <td><button class="btn btn-danger" style="padding: 5px 10px; font-size: 0.9em;" onclick="eliminarRegistro(${registro.id})">Eliminar</button></td>
        </tr>
    `).join('');
}

// Eliminar registro
function eliminarRegistro(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar este registro?')) return;

    fetch(`/api/registros/${id}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => cargarRegistros())
        .catch(error => {
            alert('Error al eliminar registro');
            console.error('Error:', error);
        });
}

// Limpiar historial
function limpiarHistorial() {
    if (!confirm('¿Estás seguro? Esto eliminará TODOS los registros.')) return;

    registros.forEach(registro => {
        fetch(`/api/registros/${registro.id}`, { method: 'DELETE' });
    });

    setTimeout(cargarRegistros, 500);
}
